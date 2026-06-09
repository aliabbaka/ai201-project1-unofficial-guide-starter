def load_and_chunk(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.split("\n")

    # Group lines into reviews. Each review starts with a line beginning
    # with "-" (the reviewer's name) and runs until the next such line.
    chunks = []
    current = []
    for line in lines:
        if line.startswith("-"):
            if current:
                chunks.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append("\n".join(current).strip())

    # Drop any empty chunks and attach the source.
    chunks = [
        {"text": text, "source": filepath}
        for text in chunks
        if text
    ]

    return chunks


if __name__ == "__main__":
    chunks = load_and_chunk("documents/CleveReviews.txt")
    print(f"Total chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks[:3]):
        print(f"--- Chunk {i+1} ---")
        print(chunk["text"][:300])
        print()
