from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyMuPDFLoader("../../data/notice.pdf")


docs = loader.load()


def validate(docs):
    empty_pages = []
    
    for d in docs:
        text = d.page_content.strip()   # 공백 제거
       
        if len(text) <10:
            page = d.metadata.get("page", "?")
            empty_pages.append(page)
    
    if empty_pages:
        print("스캔 pdf 일 수 있습니다.")    
        
        
validate(docs)
print("-"*50)
print(docs[0].metadata)
print("-"*50)
print(len(docs))
