from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from app.config import OPENAI_API_KEY, CHROMA_DB_DIR

def get_code_agent():
    db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=retriever,
        return_source_documents=True
    )
    return qa
