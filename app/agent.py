from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from app.config import settings

def get_code_agent():
    db = Chroma(persist_directory=settings.CHROMA_DB_DIR, embedding_function=OpenAIEmbeddings())

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=retriever,
        return_source_documents=True
    )
    return qa
