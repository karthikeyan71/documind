from rag.document_hash import generate_file_hash

file1 = b"Hello RAG"
file2 = b"Hello RAG"
file3 = b"Different content"

print(generate_file_hash(file1) == generate_file_hash(file2))
print(generate_file_hash(file1) == generate_file_hash(file3))