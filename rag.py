from groq import Groq
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma


# -------------------------------
# GROQ API
# -------------------------------

client = Groq(api_key="YOUR_GROQ_API_KEY")


# -------------------------------
# LOAD PDF
# -------------------------------

pdf_files = [
    "solid waste management.pdf",
    "operatingsystemnotes.pdf"
]

documents = []

for pdf in pdf_files:

    loader = PyPDFLoader(pdf)

    documents.extend(loader.load())

print("\nPDF Loaded Successfully!\n")


# -------------------------------
# SPLIT INTO CHUNKS
# -------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap=0 
)

chunks = splitter.split_documents(documents)

print(f"Total Chunks Created: {len(chunks)}\n")


# PRINT FIRST 3 CHUNKS

for i, chunk in enumerate(chunks[:3]):

    print(f"\nChunk {i+1}:\n")

    print(chunk.page_content)

    print("\n" + "="*50)


# -------------------------------
# CREATE EMBEDDINGS
# -------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

print("\nEmbeddings Created!\n")


# -------------------------------
# STORE IN CHROMADB
# -------------------------------

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)

print("\nEmbeddings Stored in ChromaDB!\n")


# -------------------------------
# CREATE RETRIEVER
# -------------------------------

retriever = db.as_retriever(
    search_kwargs={"k": 2}
)
messages = [
    {
        "role": "system",
        "content": "You are a helpful teacher AI assistant that answers using retrieved document context."
    }
]

# -------------------------------
# CHAT LOOP
# -------------------------------

while True:

    query = input("\nYou: ")

    if query.lower() == "bye":

        print("AI: Bye bestie!")

        break


    # -------------------------------
    # RETRIEVE RELEVANT CHUNKS
    # -------------------------------

    docs = retriever.invoke(query)

    print("\nRetrieved Chunks:\n")

    context = ""

    for i, doc in enumerate(docs):

        print(f"\nChunk {i+1}:\n")

        print(doc.page_content)

        print("\n" + "="*50)

        context += doc.page_content + "\n"


        # -------------------------------
    # CREATE PROMPT
    # -------------------------------

    prompt = f"""
You are a helpful teacher AI assistant.

Use the retrieved context to explain the answer clearly in simple language.

Explain in a beginner-friendly way.

If information is partially available,
answer using the available context.

Do not make up information outside the context.

Context:
{context}

Question:
{query}
"""

    # -------------------------------
    # SEND TO GROQ
    # -------------------------------
    messages.append(
    {
        "role": "user",
        "content": prompt
    }
)
    chat_completion = client.chat.completions.create(

    messages=messages,

    model="llama-3.1-8b-instant",

    temperature=0.3,

    max_tokens=300
)


    
    with open("chat_logs.txt", "a", encoding="utf-8") as log_file:

        log_file.write("\n" + "="*50 + "\n")

        log_file.write(f"Time: {datetime.now()}\n\n")

        log_file.write(f"User Question:\n{query}\n\n")

        log_file.write("Retrieved Chunks:\n")

        for i, doc in enumerate(docs):

            log_file.write(f"\nChunk {i+1}:\n")

            log_file.write(doc.page_content + "\n")

        log_file.write("\nAI Answer:\n")

        log_file.write(response + "\n")
    messages.append(
    {
        "role": "assistant",
        "content": response
    }
)

    # -------------------------------
    # PRINT FINAL ANSWER
    # -------------------------------

    print("\nAI Answer:\n")

    print(response)
    print("\nSources Used:\n")

    for i in range(len(docs)):
     print(f"Chunk {i+1}")