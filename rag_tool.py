from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from transcript_analyzer import get_academic_data


embeddings = OllamaEmbeddings(
    model="all-minilm:latest"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)

llm = ChatOllama(
    model="qwen3:0.6b"
)


def answer_question(question):

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    academic_data = get_academic_data(
        "documents/transcript.pdf"
    )

    academic_context = "\n".join(
        f"{subject}: {marks}/100"
        for subject, marks in academic_data.items()
    )

    prompt = f"""
You are StudyPilot AI, a personalized education assistant.

Use BOTH:
1. The student's academic performance
2. The retrieved study material

Student academic performance:
{academic_context}

Retrieved study material:
{context}

Student question:
{question}

Give a clear, useful and personalized answer.
If the question is about the student's performance,
use the academic performance data.
If the question is about study material,
use the retrieved study material.
Do not invent marks or academic information.
"""

    response = llm.invoke(prompt)

    return response.content