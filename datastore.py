import os
import shutil
from pathlib import Path
from typing import List

import mesop as me
from embeddings import Embeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from retriever import Retriever


class DataStoreGenerator:
    CHROMA_PATH = "chroma"
    DATA_PATH = Path("data/uploaded_docs")
    retriever = None

    @classmethod
    def process_files(cls, files: List[me.UploadedFile], overwrite: bool = False, chunk_size: int = 300, chunk_overlap: int = 100):
        if not overwrite and os.path.exists(cls.CHROMA_PATH):
            db = Chroma(persist_directory=cls.CHROMA_PATH, embedding_function=Embeddings.get_embeddings())
            cls.retriever = Retriever(db)
            print(f"Data store already exists at {cls.CHROMA_PATH}. Use overwrite=True to recreate.")
            return

        cls._save_files(files)
        documents = []
        for file in files:
            doc = Document(
                page_content=file.getvalue(),
                metadata={"source": str(f"{file.name}")}
            )
            documents.append(doc)
        chunks = cls._split_text(documents, chunk_size, chunk_overlap)
        cls._save_to_chroma(chunks, overwrite)

    
        
    @classmethod
    def _save_files(cls, files: List[me.UploadedFile], file_path: Path = DATA_PATH):
        # Ensure the parent directory exists, create it if it does not
        if not file_path.exists():
            file_path.mkdir(parents=True, exist_ok=True)

        file_paths = []
        for file in files:
            if file is not None:
                dest_path = file_path / file.name
                
                # Write the uploaded file content to the destination path
                with open(dest_path, 'wb') as f:
                    f.write(file.getvalue())
                    
                file_paths.append(str(dest_path))
        
        if file_paths:
            return f"Files uploaded successfully: {', '.join(file_paths)}"
        return "No files uploaded."
    
    
    @classmethod
    def _split_text(cls, documents: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        if chunks:
            document = chunks[10]
            print(document.page_content)
            print(document.metadata)
        return chunks

    @classmethod
    def _save_to_chroma(cls, chunks: List[Document], overwrite: bool):
        if overwrite and os.path.exists(cls.CHROMA_PATH):
            shutil.rmtree(cls.CHROMA_PATH)
        
        hf = Embeddings.get_embeddings()
        db = Chroma.from_documents(
            chunks, hf, persist_directory=cls.CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {cls.CHROMA_PATH}.")
        cls.retriever = Retriever(db)


if __name__ == "__main__":
    data_path = Path("data")
    DataStoreGenerator.process_files(data_path, overwrite=False)