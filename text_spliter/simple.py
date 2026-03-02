from abc import ABC, abstractmethod


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
    def __init__(self, separators: list[str], chunk_size: int, overlap_count: int = 0):
        super().__init__(chunk_size, overlap_count)
        self.separators = separators or ["\n\n", "\n", "。", "！", "？", "，", "、", "；", "：", " "]

    def split_text(self, text: str) -> list[str]:
        return self.__recursive_split(text, 0)

    def __recursive_split(self, text: str, separators_index: int) -> list[str]:
        # BUG: `chunks = []` is declared but never used in the return path
        # when separators are exhausted or text fits in chunk_size; remove it.
        if separators_index >= len(self.separators):
            simple_splitter = SimpleTextSplitter(self.chunk_size, self.overlap_count)
            return simple_splitter.split_text(text)

        if len(text) <= self.chunk_size:
            return [text]

        # BUG: `text.split(sep)` discards the separator itself, so punctuation like
        # "。" "，" is lost from the output. After splitting, re-attach the separator
        # to the end of each part (except the last) to preserve sentence boundaries.
        split_text = text.split(self.separators[separators_index])

        # BUG: loop variable `text` shadows the parameter `text`, which is confusing
        # and error-prone. Rename to `part` or `segment`.
        for segment in split_text:
            # BUG: empty strings produced by split (e.g. leading/trailing separator)
            # are appended as-is. Add `if not text: continue` to skip them.
            segment = segment + self.separators[separators_index]
            if len(text) <= self.chunk_size:
                chunks.append(text)
            else:
                chunks.extend(self.__recursive_split(text, separators_index + 1))

        # MISSING: after recursion, small segments are not merged together.
        # Many chunks will be far smaller than chunk_size.
        # Add a `__merge_segments` call here to greedily combine small segments
        # into full-sized chunks before returning.
        return chunks

    # MISSING: implement `__merge_segments(self, segments: list[str]) -> list[str]`
    #
    # Use a sliding-window approach (same as LangChain's _merge_splits):
    #   - maintain `current_doc: list[str]` and `total: int` (sum of lengths)
    #   - for each segment:
    #       - if total + len(seg) > chunk_size and current_doc is non-empty:
    #           - join current_doc and append to chunks
    #           - slide: pop from the front of current_doc while total > overlap_count
    #             (this leaves the tail of the previous chunk as the overlap prefix
    #              for the next chunk — overlap consists of complete semantic segments,
    #              not a hard character slice)
    #       - append seg to current_doc, add its length to total
    #   - after the loop, join and append whatever remains in current_doc


if __name__ == "__main__":
    text = """
    Hello, world!
This is a test text. It is used to test the text splitter. It is a simple text splitter. It is a recursive text splitter, and it is a simple text splitter.
    我是中国人，我喜欢吃米饭。你是哪里人？你喜欢吃什么？ 天气很好，我喜欢出去玩。你觉得呢？ 如果你喜欢，请点赞。
    """
    # splitter = RecursiveTextSplitter(separators=["\n\n", "\n", "。", "！", "？", "，", "、", "；", "："], chunk_size=20, overlap_count=2)
    # chunks = splitter.split_text(text)
    # print(chunks)
    test_text = "我是中国人，我喜欢吃米饭。你是哪里人？你喜欢吃什么？ 天气很好，我喜欢出去玩。你觉得呢？ 如果你喜欢，请点赞。"
    list_text = list(test_text)
    length = len(list_text)
    print(length)

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=22, chunk_overlap=2)
    chunks = splitter.split_text(text)
    print(chunks)
