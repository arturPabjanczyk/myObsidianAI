import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", ".")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
DOCS_DIR = os.path.join(DATA_DIR, "docs")

loader = DirectoryLoader(
    DOCS_DIR,
    glob="**/*",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory=CHROMA_DIR
)
if hasattr(vectorstore, "persist"):
    vectorstore.persist()

print("OK: ingest done")