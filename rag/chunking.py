def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks


document = """
Our application supports password reset.
Users can request a reset link through the login page.
The link expires after 30 minutes.
Users must create a password containing at least 12 characters.
"""

chunks = chunk_text(document, chunk_size=15, overlap=3)

for index, chunk in enumerate(chunks):
    print(f"Chunk {index + 1}: {chunk}")