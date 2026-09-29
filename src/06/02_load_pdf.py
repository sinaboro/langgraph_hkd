from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyMuPDFLoader("../../data/notice.pdf")


documents = loader.load()

# 문서를 청크로 나누기

splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)

chunks = splitter.split_documents(documents)

print(f'청크 사이즈 : {len(chunks)}')
print("-"*50)
print(chunks[0].page_content)
print("-"*50)
print(chunks[1].page_content)
print("-"*50)

