from langchain_community.document_loaders import PyMuPDFLoader
import os
import re

"""
    pdf 문서 마다 불필요한 noise가 있다면 , 그 noise를 제거 하는 
    프로그램
"""

NOISE = ["대외비"]

def load_documents(path):
    loader = PyMuPDFLoader(path)
    
    docs = loader.load()
    
    for d in docs:
    
        text = d.page_content
        
        # noise 제거 하는 코드 
        for noise in NOISE:
            text = text.replace(noise, "")
        
        # 줄바꿈이 3개 이상 연속으로 있으면 줄바꿈 2개로 줄여라.
        text =  re.sub(r"\n{3,}", "\n\n", text)
        
        d.page_content = text.strip()
        
        # 메타 데이터        
        d.metadata["filename"]  = os.path.basename(path)
        d.metadata["page_no"] = d.metadata.get("page", 0) + 1
        
    empty_pages = []
        
    for d in docs:
        text = d.page_content.strip()   # 공백 제거
        
        if len(text) <10:
            page = d.metadata.get("page", "?")
            empty_pages.append(page)

    if empty_pages:
        print("스캔 pdf 일 수 있습니다.")  
    
    total_len = 0
    
    for d in docs:
        total_len += len(d.page_content) 
    
    print(f"{len(docs)}쪽 로딩 완료 (총{total_len}자)")       
    
    return docs

if __name__ == "__main__":
    path = "../../data/manual.pdf"
    docs = load_documents(path)
    print(docs[0].page_content)


