from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

PDF_PATH = "documents/transcript.pdf"

# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"Pages loaded: {len(documents)}")

# 2. Split the document into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")

# 3. Create embeddings using Ollama
embeddings = OllamaEmbeddings(
    model="all-minilm:latest"
)

# 4. Store embeddings in Chroma
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("RAG database created successfully!")
# 5. Test retrieval
query = "Which subjects need the most improvement?"

results = vector_store.similarity_search(query, k=2)

print("\n--- RETRIEVED INFORMATION ---")

for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(doc.page_content)