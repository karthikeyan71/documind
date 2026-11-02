import ollama

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.database import engine
from rag.document_storage import DocumentChunk


def retrieve_chunks(question, limit=2):

    # Generate question embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = response["embeddings"][0]

    # Retrieve relevant chunks
    with Session(engine) as session:

        statement = (
            select(DocumentChunk.chunk_text)
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    question_embedding
                )
            )
            .limit(limit)
        )

        results = session.scalars(statement).all()

    return results


def generate_answer(question, context):

    prompt = f"""
    You are a document question-answering assistant.

    Rules:
    1. Answer strictly using the provided context.
    2. Do not make assumptions or use outside knowledge.
    3. Distinguish between facts explicitly stated
    and conclusions that are not supported.
    4. If the context does not explicitly answer the question,
    say: "The provided document does not contain this information."
    5. Do not infer that something is impossible just because
    the document does not mention it.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    return response["message"]["content"]


if __name__ == "__main__":

    # question = "How long is my password reset link valid?"
    question = "Can I extend my password reset link to 2 hours?"

    # 1. Retrieval
    chunks = retrieve_chunks(question)

    context = "\n".join(chunks)

    print("\nRetrieved context:")
    print(context)

    # 2. Generation
    answer = generate_answer(question, context)

    print("\nGenerated answer:")
    print(answer)