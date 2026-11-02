
import ollama

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    select
)

from sqlalchemy.orm import Session, relationship
from pgvector.sqlalchemy import Vector

from db.database import engine, Base
from rag.document_hash import generate_file_hash


# -------------------------
# Document Model
# -------------------------

class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False, unique=True)
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


# -------------------------
# Document Chunk Model
# -------------------------

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    document_id = Column(
        BigInteger,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=True
    )

    document_name = Column(String(255), nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)

    document = relationship(
        "Document",
        back_populates="chunks"
    )


# -------------------------
# Find Document
# -------------------------

def get_document_by_filename(filename: str):
    with Session(engine) as session:
        statement = select(Document).where(
            Document.filename == filename
        )

        return session.scalar(statement)


# -------------------------
# Save Document
# -------------------------

def save_document(chunks, filename, file_bytes):

    content_hash = generate_file_hash(file_bytes)

    with Session(engine) as session:

        document = session.scalar(
            select(Document).where(
                Document.filename == filename
            )
        )

        # Scenario 1: Same filename and identical content
        if document and document.content_hash == content_hash:
            return {
                "status": "skipped",
                "message": "Document already exists with identical content"
            }

        # Generate embeddings
        response = ollama.embed(
            model="nomic-embed-text",
            input=chunks
        )

        embeddings = response["embeddings"]

        # Scenario 2: Same filename, modified content
        if document:
            status = "replaced"

            document.chunks.clear()

            document.content_hash = content_hash
            document.updated_at = datetime.now(timezone.utc)

        # Scenario 3: New filename
        else:
            status = "created"

            document = Document(
                filename=filename,
                content_hash=content_hash,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            session.add(document)

        # Attach new chunks to document
        for chunk, embedding in zip(chunks, embeddings):

            document.chunks.append(
                DocumentChunk(
                    document_name=filename,
                    chunk_text=chunk,
                    embedding=embedding
                )
            )

        session.commit()

        return {
            "status": status,
            "message": "Document processed successfully",
            "total_chunks": len(chunks)
        }
