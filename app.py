import os
from dotenv import load_dotenv
import chainlit as cl
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", ".")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template = """Jesteś asystentem szkolnego archiwum.
Odpowiedz na pytanie tylko na podstawie poniższego kontekstu:
{context}

Pytanie: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

@cl.on_message
async def main(message: cl.Message):
    response = rag_chain.invoke(message.content)
    await cl.Message(content=response).send()