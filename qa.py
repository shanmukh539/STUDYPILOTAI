from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

# Embedding model
embeddings = OllamaEmbeddings(
    model="all-minilm:latest"
)

# Load our existing Chroma database
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

# Our local LLM
llm = ChatOllama(
    model="qwen3:0.6b"
)

# Student question
question = "Which subjects need the most improvement?"

# Retrieve relevant information
documents = retriever.invoke(question)

context = "\n\n".join(
    document.page_content for document in documents
)

# Give retrieved information to the LLM
prompt = f"""
You are an education assistant.

Answer the student's question using ONLY the information
provided in the transcript context below.

Transcript context:
{context}

Student question:
{question}

Give a clear and simple answer.
"""

response = llm.invoke(prompt)

print("\n--- RAG ANSWER ---")
print(response.content)