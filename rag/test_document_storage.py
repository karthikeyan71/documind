from rag.document_storage import save_document

file1 = b"Employee policy version 1"
file2 = b"Employee policy version 1"
file3 = b"Employee policy version 2"

chunks1 = [
    "Employees receive 20 days of annual leave.",
    "Unused leave can be carried forward."
]

chunks3 = [
    "Employees receive 25 days of annual leave.",
    "Unused leave cannot be carried forward."
]

# Scenario 1: New document
print(save_document(chunks1, "policy.pdf", file1))

# Scenario 2: Same filename and same content
print(save_document(chunks1, "policy.pdf", file2))

# Scenario 3: Same filename but modified content
print(save_document(chunks3, "policy.pdf", file3))