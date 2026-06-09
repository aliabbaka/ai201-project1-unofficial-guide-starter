import re

def load_and_chunk(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    # Split on lines that start with a dash followed by a name (e.g. "-Mariah Sprague")
    parts = re.split(r'\n(?=-\w)', raw)

    chunks = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        chunks.append({
            "text": part,
            "source": filepath
        })

    return chunks

if __name__ == "__main__":
    chunks = load_and_chunk("documents/CleveReviews.txt")
    print(f"Total chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks[:3]):
        print(f"--- Chunk {i+1} ---")
        print(chunk["text"][:300])
        print()