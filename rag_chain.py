from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.embeddings import OllamaEmbeddings  # optional if you use embeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader, PyMuPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings




import os

def load_and_embed(file_path: str, persist_directory: str = "chroma_db"):
    if file_path.endswith(".pdf"):
        loader = PyMuPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # You can still use OpenAIEmbeddings or switch to local Ollama embeddings later
    embeddings = OllamaEmbeddings(model="mistral:latest")
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()

    return vectordb

def get_retriever(persist_directory: str = "chroma_db"):
    embeddings = OllamaEmbeddings(model="mistral:latest")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb.as_retriever()

def answer_query(retriever, question: str):
    llm = Ollama(model="mistral")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)

def generate_summary(topic: str):
    llm = Ollama(model="mistral")
    prompt = f"Give me a short and clear summary on the topic: {topic} in under 100 words."
    return llm.invoke(prompt)

def generate_mcqs(topic: str, num_questions: int = 3):
    llm = Ollama(model="mistral")
    prompt = (
        f"Generate exactly {num_questions} multiple choice questions on the topic '{topic}'. "
        f"Each question must have 4 options (A, B, C, D), and clearly state the correct answer as 'Answer: X'. "
        f" Number the questions from 1 to {num_questions}. Do not skip any. Output only the questions."
    )
    return llm.invoke(prompt)



def generate_explanation(topic: str):
    llm = Ollama(model="mistral")
    prompt = f"Explain the topic '{topic}' in a step-by-step, beginner-friendly way."
    return llm.invoke(prompt)
