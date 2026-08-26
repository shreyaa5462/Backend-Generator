from uuid import uuid4

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class RAGService:

    _embeddings = None

    @staticmethod
    def get_embeddings():

        if RAGService._embeddings is None:

            print(
                "Loading embedding model..."
            )

            RAGService._embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            print(
                "Embedding model loaded."
            )

        return RAGService._embeddings

    @staticmethod
    def create_retriever(
        document_text: str
    ):

        # -----------------------------------------
        # 1. Split document into chunks
        # -----------------------------------------

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        documents = splitter.create_documents(
            [document_text]
        )

        print(
            f"RAG: created {len(documents)} chunks"
        )

        # -----------------------------------------
        # 2. Create Chroma vector store
        # -----------------------------------------

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=RAGService.get_embeddings(),
            collection_name=f"srd_{uuid4().hex}"
        )

        print(
            "RAG: vector store created"
        )

        # -----------------------------------------
        # 3. Create retriever
        # -----------------------------------------

        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 3
            }
        )

        return retriever

    @staticmethod
    def get_context(
        retriever,
        query: str,
        max_chars: int = 6000
    ) -> str:

        # -----------------------------------------
        # 1. Retrieve relevant chunks
        # -----------------------------------------

        documents = retriever.invoke(
            query
        )

        # -----------------------------------------
        # 2. Build context
        # -----------------------------------------

        context_parts = []

        total_chars = 0

        for document in documents:

            text = document.page_content.strip()

            if not text:
                continue

            remaining_chars = (
                max_chars - total_chars
            )

            if remaining_chars <= 0:
                break

            text = text[:remaining_chars]

            context_parts.append(
                text
            )

            total_chars += len(text)

        context = "\n\n".join(
            context_parts
        )

        print(
            f"RAG: retrieved {len(documents)} chunks"
        )

        print(
            f"RAG: context size = {len(context)} characters"
        )

        return context