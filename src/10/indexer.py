import datetime
import json

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

import os
import sys

"""
    이 프로그램 용도는
    저장한 faiss_index 파일이 오래되면 이 용도가 기억이 안날 수 있다
    따라서 이 용도가 무엇인지 json파일로 저장하는 것이다.
"""


CURRENT_DIR = os.path.dirname(__file__)
PREPARE_DIR = os.path.join(CURRENT_DIR, "..", "07")
sys.path.insert(0, PREPARE_DIR)
from prepare import prepare_chunk

load_dotenv()

DOC_PATH = "../../data/manual.pdf"
INDEX_PATH = "faiss_index"
EMBED_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def save_with_meta(store, path, info):
    store.save_local(path)
    info["created_at"] = datetime.datetime.now().isoformat()
    meta_path = os.path.join(path, "build_info.json")
    
    with open(meta_path, "w", encoding="utf-8") as file:
        json.dump(
            info,
            file,
            ensure_ascii=False,
            indent=2
        )

def get_store(rebuild=False):
    emb = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(INDEX_PATH) and not rebuild:
        store = FAISS.load_local(
            INDEX_PATH,
            emb,
            allow_dangerous_deserialization=True
        )
        return store

    chunks = prepare_chunk(DOC_PATH)

    store = FAISS.from_documents(
        chunks,
        emb
    )

    build_info = {
        "source": DOC_PATH,
        "embed_model": EMBED_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "chunk_count": len(chunks),
    }

    save_with_meta(store, INDEX_PATH, build_info)

    print("저장 완료........")
    
    return store

if __name__ == "__main__":
    store = get_store()

