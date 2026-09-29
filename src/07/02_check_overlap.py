from langchain_community.document_loaders import PyMuPDFLoader
import os, sys,re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 현재 디렉토리
CURRENT_DIR = os.path.dirname(__file__)
INGEST_DIR = os.path.join(CURRENT_DIR, "..", "06")
sys.path.insert(0, INGEST_DIR)

from ingest import load_documents

docs = load_documents("../../data/manual.pdf")

splitter =RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20,
    separators=["\n\n", "\n", ".", " "],
    length_function = len
)

chunks = splitter.split_documents(docs)

full_text = ""

for doc in docs:
    full_text += doc.page_content + "\n\n"    
    

merged_doc = Document(page_content = full_text)

chunks = splitter.split_documents([merged_doc])
    
# 겹쳐진 청크 사이즈 확인 함수
def show_boundary(chuks, index=0):
    print("-"*50)
    print(chunks[index].page_content)
    print("-"*50)
    print(chunks[index+1].page_content)
    
    
show_boundary(chunks)