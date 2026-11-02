import ollama

response = ollama.embed(
    model="nomic-embed-text",
    input="How do I reset my password?"
)

embedding = response["embeddings"][0]

print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
