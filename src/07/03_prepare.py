from langchain_community.document_loaders import PyMuPDFLoader
import os, sys,re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# 현재 디렉토리
CURRENT_DIR = os.path.dirname(__file__)
INGEST_DIR = os.path.join(CURRENT_DIR, "..", "06")
sys.path.insert(0, INGEST_DIR)
from ingest import load_documents

CHUNK_SISE = 200
CHUNK_OVERLAP = 50

def prepare_chunk(path):
    docs = load_documents(path)    

    splitter =RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SISE,
        chunk_overlap = CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
        length_function = len
    )
    
    chunks = splitter.split_documents(docs)
    
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index
    
    print(f'청크 {len(chunks)}개')
    
    return chunks

if __name__ == "__main__":   
    chunks = prepare_chunk("../../data/manual.pdf")
    
    for chunk in chunks[:3]:
        print(chunk.page_content)
        print("-"*50)
        print("chunk_id : ", chunk.metadata['chunk_id'])
        print("-"*100)