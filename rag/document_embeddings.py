import ollama
from chunking import chunk_text

document = """
Our application supports password reset.
Users can request a reset link through the login page.
The link expires after 30 minutes.
Users must create a password containing at least 12 characters.
"""

# Step 1: Split document into chunks
chunks = chunk_text(
    document,
    chunk_size=15,
    overlap=3
)

# Step 2: Generate embeddings for each chunk
response = ollama.embed(
    model="nomic-embed-text",
    input=chunks
)

embeddings = response["embeddings"]

# Step 3: Display results
for index, chunk in enumerate(chunks):
    print(f"\nChunk {index + 1}: {chunk}")
    print("Embedding dimensions:", len(embeddings[index]))