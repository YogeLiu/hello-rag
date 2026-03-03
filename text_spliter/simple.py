from math import floor
from sentence_transformers import SentenceTransformer
from abc import ABC, abstractmethod
from typing import Any
import re
import numpy as np

from torch.nn.functional import embedding


class TextSplitter(ABC):
    def __init__(self, chunk_size: int, overlap_count: int = 0):
        self.chunk_size = chunk_size
        self.overlap_count = overlap_count

    @abstractmethod
    def split_text(self, text: str) -> list[str]:
        pass


class SimpleTextSplitter(TextSplitter):
    def __init__(self, chunk_size: int, overlap_count: int = 0):
        super().__init__(chunk_size, overlap_count)

    def split_text(self, text: str) -> list[str]:
        words = list(text)
        chunks = []
        step = self.chunk_size - self.overlap_count
        if step <= 0:
            step = 1

        for i in range(0, len(words), step):
            chunk = "".join(words[i : i + self.chunk_size])
            if chunk:
                chunks.append(chunk)
            if i + self.chunk_size >= len(words):
                break

        return chunks


class RecursiveTextSplitter(TextSplitter):
    def __init__(self, separators: list[str], chunk_size: int, overlap_count: int = 0, is_separator_regex: bool = False):
        super().__init__(chunk_size, overlap_count)
        self.separators = separators or ["\n\n", "\n", " ", ""]
        self.is_separator_regex = is_separator_regex

    def split_text(self, text: str) -> list[str]:
        return self.__recursive_split(text, self.separators)

    def __merge_segments(self, segments: list[str], separator: str) -> list[str]:
        """Merge small segments into chunks that meet size requirements.

        This method re-inserts the separator between segments to preserve
        the original text structure (spaces, newlines, etc.).

        Args:
            segments: List of text segments to merge
            separator: The separator to use when joining segments

        Returns:
            List of merged text chunks
        """
        docs = []
        current_doc = []
        total = 0
        sep_len = len(separator)

        for segment in segments:
            seg_len = len(segment)
            # Calculate the length if we add this segment
            # If current_doc is not empty, we need to add separator length
            added_length = seg_len + (sep_len if len(current_doc) > 0 else 0)

            # Check if adding this segment would exceed chunk_size
            if total + added_length > self.chunk_size:
                # Save current doc if not empty
                if len(current_doc) > 0:
                    docs.append(separator.join(current_doc))
                    # Handle overlap: remove from the beginning until we meet overlap requirement
                    # OR until we have room for the new segment
                    while total > self.overlap_count or (total + seg_len + (sep_len if len(current_doc) > 0 else 0) > self.chunk_size and total > 0):
                        # Remove the first segment
                        total -= len(current_doc[0]) + (sep_len if len(current_doc) > 1 else 0)
                        current_doc = current_doc[1:]

            current_doc.append(segment)
            # Update total: add segment length + separator length if not first segment
            total += seg_len + (sep_len if len(current_doc) > 1 else 0)

        # Append remaining segments
        if current_doc:
            docs.append(separator.join(current_doc))

        return docs

    def __recursive_split(self, text: str, separators: list[str]) -> list[str]:
        """Recursively split text using a hierarchy of separators.

        Args:
            text: The text to split
            separators: List of separators to try, in order of preference

        Returns:
            List of text chunks
        """
        # Default to the last separator
        separator = separators[-1]
        new_separators = []

        # Find the first separator that exists in the text
        for i, s_ in enumerate(separators):
            separator_ = s_ if self.is_separator_regex else re.escape(s_)
            if not s_:
                # Empty separator means split by character
                separator = s_
                break

            if re.search(separator_, text):
                separator = s_
                new_separators = separators[i + 1 :]
                break

        # Split the text using the chosen separator
        separator_regex = separator if self.is_separator_regex else re.escape(separator)
        if separator == "":
            # Split by character
            segments = list(text)
        else:
            # Split by separator and filter out empty strings
            segments = [s for s in re.split(separator_regex, text) if s]

        # When merging, determine what to use as separator:
        # - For regex separators: use empty string (can't reconstruct the exact matched char)
        # - For literal separators: use the separator itself to preserve structure
        if self.is_separator_regex:
            merge_separator = ""
        else:
            merge_separator = separator

        final_chunks = []
        good_chunks = []

        for segment in segments:
            if len(segment) <= self.chunk_size:
                # Segment is small enough, collect it
                good_chunks.append(segment)
            else:
                # Segment is too large, need to handle it
                if good_chunks:
                    # First, merge all collected good chunks
                    final_chunks.extend(self.__merge_segments(good_chunks, merge_separator))
                    good_chunks = []

                # Now handle the large segment
                if not new_separators:
                    # No more separators to try, must include as-is (exceeds chunk_size)
                    final_chunks.append(segment)
                else:
                    # Try splitting with finer-grained separators
                    final_chunks.extend(self.__recursive_split(segment, new_separators))

        # Don't forget remaining good chunks
        if good_chunks:
            final_chunks.extend(self.__merge_segments(good_chunks, merge_separator))

        return final_chunks


class SemanticTextSplitter(TextSplitter):
    """Semantic text splitter using embedding similarity to find natural breakpoints.

    Based on Greg Kamradt's semantic chunking algorithm. This splitter:
    1. Splits text into sentences
    2. Groups sentences together (buffer_size sentences per group)
    3. Calculates embeddings for each sentence
    4. Computes similarity between adjacent sentences
    5. Identifies breakpoints where similarity drops significantly
    6. Merges sentences into chunks at breakpoints

    References:
        - Greg Kamradt's "5 Levels of Text Splitting"
        - LangChain SemanticChunker implementation
    """

    def __init__(
        self, chunk_size: int = 1000, buffer_size: int = 1, breakpoint_type: str = "percentile", model_name: str = "sentence-transformers/all-MiniLM-L6-v2", breakpoint_threshold: float = 95.0
    ):
        """Initialize semantic text splitter.

        Args:
            chunk_size: Maximum size of each chunk (soft limit)
            buffer_size: Number of sentences to group together for comparison
                        1 = compare individual sentences (default)
                        3 = compare sentence triplets (more stable)
            breakpoint_type: Method to calculate breakpoint threshold
                           "percentile" = use percentile of distances (default)
                           "std" = use standard deviation
                           "interquartile" = use interquartile range
                           "gradient" = use gradient of distances
            model_name: Sentence transformer model name
            breakpoint_threshold: Threshold value for breakpoint detection
                                 For percentile: 95 means split at top 5% distance changes
                                 For std: number of standard deviations from mean
        """
        super().__init__(chunk_size)
        self.buffer_size = buffer_size
        self.model = SentenceTransformer(model_name)
        self.breakpoint_type = breakpoint_type
        self.breakpoint_threshold = breakpoint_threshold

    def split_text(self, text: str) -> list[str]:
        """Split text into semantically coherent chunks."""
        sentences = self.__split_sentences(text)

        if len(sentences) <= 1:
            return sentences

        combined_sentences = self.__combine_sentences(sentences)
        embeddings = self.model.encode([s["combined_sentence"] for s in combined_sentences])

        similarities = self.__calculate_similarities(embeddings)

        breakpoint_indices = self.__find_breakpoints(similarities)

        chunks = self.__create_chunks(sentences, breakpoint_indices)

        return self.__enforce_chunk_size(chunks)

    def __split_sentences(self, text: str) -> list[str]:
        """Split text into sentences using regex for both English and Chinese."""
        sentence_endings = r'(?<=[.!?。！？])\s+'
        sentences = re.split(sentence_endings, text)

        result = [s.strip() for s in sentences if s.strip()]
        return result if result else [text]

    def __combine_sentences(self, sentences: list[str]) -> list[dict[str, Any]]:
        """Combine sentences into groups for more stable embedding comparison.

        For buffer_size=1: each group is a single sentence
        For buffer_size=3: each group is 3 consecutive sentences (overlapping)

        Returns:
            List of dicts with 'combined_sentence', 'index', and 'sentence'
        """
        combined = []

        for i, sentence in enumerate(sentences):
            start_idx = max(0, i - self.buffer_size)
            end_idx = min(len(sentences), i + self.buffer_size + 1)

            sentences_to_combine = sentences[start_idx:end_idx]
            combined_sentence = " ".join(sentences_to_combine)

            combined.append({"combined_sentence": combined_sentence, "index": i, "sentence": sentence})

        return combined

    def __calculate_similarities(self, embeddings: np.ndarray) -> list[float]:
        """Calculate cosine similarity between adjacent embeddings."""
        similarities = []

        for i in range(len(embeddings) - 1):
            similarity = self.__cosine_similarity(embeddings[i], embeddings[i + 1])
            similarities.append(similarity)

        return similarities

    def __cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.

        Returns value between -1 and 1, where:
            1 = identical direction (most similar)
            0 = orthogonal (unrelated)
           -1 = opposite direction (most dissimilar)
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def __calculate_threshold(self, similarities: list[float]) -> float:
        """Calculate breakpoint threshold based on breakpoint_type.

        For percentile: lower similarities (below threshold percentile) indicate breakpoints
        """
        if self.breakpoint_type == "percentile":
            return np.percentile(similarities, 100 - self.breakpoint_threshold)

        elif self.breakpoint_type == "std":
            mean_sim = np.mean(similarities)
            std_sim = np.std(similarities)
            return mean_sim - (self.breakpoint_threshold * std_sim)

        elif self.breakpoint_type == "interquartile":
            q1 = np.percentile(similarities, 25)
            q3 = np.percentile(similarities, 75)
            iqr = q3 - q1
            return q1 - (self.breakpoint_threshold * iqr)

        elif self.breakpoint_type == "gradient":
            gradient = np.gradient(similarities)
            abs_gradient = np.abs(gradient)
            threshold_gradient = np.percentile(abs_gradient, self.breakpoint_threshold)

            breakpoint_similarity = np.mean(similarities)
            return breakpoint_similarity

        else:
            return np.percentile(similarities, 100 - self.breakpoint_threshold)

    def __find_breakpoints(self, similarities: list[float]) -> list[int]:
        """Find sentence indices where breakpoints should occur.

        Breakpoints occur where similarity is BELOW the threshold,
        indicating a semantic shift between sentences.
        """
        threshold = self.__calculate_threshold(similarities)
        breakpoint_indices = []

        for i, similarity in enumerate(similarities):
            if similarity < threshold:
                breakpoint_indices.append(i + 1)

        return breakpoint_indices

    def __create_chunks(self, sentences: list[str], breakpoint_indices: list[int]) -> list[str]:
        """Create chunks by grouping sentences between breakpoints."""
        chunks = []
        start_idx = 0

        for breakpoint_idx in breakpoint_indices:
            chunk_sentences = sentences[start_idx:breakpoint_idx]
            if chunk_sentences:
                chunks.append(" ".join(chunk_sentences))
            start_idx = breakpoint_idx

        remaining_sentences = sentences[start_idx:]
        if remaining_sentences:
            chunks.append(" ".join(remaining_sentences))

        return chunks

    def __enforce_chunk_size(self, chunks: list[str]) -> list[str]:
        """Ensure chunks respect chunk_size by splitting large chunks.

        This is a soft enforcement: semantic chunks are preserved where possible,
        but chunks exceeding chunk_size are split by words.
        """
        final_chunks = []

        for chunk in chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                words = chunk.split()
                current = []
                current_length = 0

                for word in words:
                    word_len = len(word)
                    space_len = 1 if current else 0

                    if current_length + word_len + space_len > self.chunk_size:
                        if current:
                            final_chunks.append(" ".join(current))
                        current = [word]
                        current_length = len(word)
                    else:
                        current.append(word)
                        current_length += word_len + space_len

                if current:
                    final_chunks.append(" ".join(current))

        return final_chunks
