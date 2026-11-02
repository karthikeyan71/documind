from rag.schemas import ChatRequest, ChatResponse
from rag.retrieval import retrieve_chunks, generate_answer

from fastapi import APIRouter, UploadFile, File, HTTPException

from rag.document_extraction import extract_pdf_text
from rag.chunking import chunk_text
from rag.document_storage import save_document

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    file_bytes = await file.read()

    text = extract_pdf_text(file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in PDF"
        )

    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50
    )

    result = save_document(
        chunks,
        file.filename,
        file_bytes
    )

    return {
        "filename": file.filename,
        **result
    }

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question

    # Retrieve relevant document chunks
    chunks = retrieve_chunks(question)

    context = "\n".join(chunks)

    # Generate answer using LLM
    answer = generate_answer(question, context)

    return ChatResponse(
        question=question,
        answer=answer
    )