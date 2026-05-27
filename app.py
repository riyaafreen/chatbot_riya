import streamlit as st

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# -------------------------------
# CUSTOM UI DESIGN
# -------------------------------

st.markdown(
    """
    <style>

    .stApp {
    background: linear-gradient(to right, #4568DC, #B06AB3);
    color: white;
      }

    h1 {
        color: #22D3EE;
        text-align: center;
        font-size: 60px;
        text-shadow: 0px 0px 15px #22D3EE;
    }

    h4 {
        text-align: center;
        color: #E2E8F0;
    }

    .stTextInput > div > div > input {
        background-color: #1E293B;
        color: white;
        border: 2px solid #22D3EE;
        border-radius: 15px;
        padding: 15px;
        font-size: 18px;
    }

    .stTextInput label {
        color: white !important;
        font-size: 18px;
    }

    .chat-box {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        background-color: #1E293B;
        box-shadow: 0px 0px 10px rgba(34,211,238,0.4);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------
# PAGE TITLE
# -------------------------------

st.title("🤖 AI Powered RAG Chatbot")

st.markdown(
    """
    <h4 style="
        text-align:left;
        color:#E2E8F0;
        margin-left:10px;
        font-size:28px;
        font-weight:500;
    ">
    AI-Powered Knowledge Retrieval from Documents 
    </h4>
    """,
    unsafe_allow_html=True
)


# -------------------------------
# GROQ API
# -------------------------------

client = Groq(
   api_key="YOUR_GROQ_API_KEY"
)


# -------------------------------
# SIDEBAR PDF SECTION
# -------------------------------

st.sidebar.title("📂 PDF Files")


# -------------------------------
# PDF UPLOAD SIDEBAR
# -------------------------------

st.sidebar.title("📂 Upload PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Upload your PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# Default PDFs already present
pdf_files = [
    "solid waste management.pdf",
    "operatingsystemnotes.pdf"
]

documents = []

# -------------------------------
# LOAD DEFAULT PDFs
# -------------------------------

for pdf in pdf_files:

    loader = PyPDFLoader(pdf)

    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = pdf

    documents.extend(docs)

# -------------------------------
# LOAD UPLOADED PDFs
# -------------------------------

if uploaded_files:

    for uploaded_file in uploaded_files:

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        loader = PyPDFLoader(uploaded_file.name)

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = uploaded_file.name

        documents.extend(docs)


# SHOW PDF NAMES IN SIDEBAR

st.sidebar.subheader("Available PDFs")

for pdf in pdf_files:

    st.sidebar.write("📄", pdf)

if uploaded_files:

    for file in uploaded_files:

        st.sidebar.write("📄", file.name)

# -------------------------------
# SPLIT INTO CHUNKS
# -------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)


# -------------------------------
# CREATE EMBEDDINGS
# -------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# -------------------------------
# STORE IN CHROMADB
# -------------------------------

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="chroma_db"
)


# -------------------------------
# CREATE RETRIEVER
# -------------------------------

retriever = db.as_retriever(
    search_kwargs={"k": 4}
)

# -------------------------------
# CHAT HISTORY
# -------------------------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# -------------------------------
# USER INPUT
# -------------------------------

st.markdown(
    """
    <style>

    .stChatInputContainer {
        position: fixed;
        bottom: 20px;
        left: 320px;
        right: 40px;
        background-color: #111827;
        padding: 10px;
        border-radius: 20px;
        border: 2px solid #22D3EE;
        z-index: 9999;
        box-shadow: 0px 0px 15px rgba(34,211,238,0.5);
    }

    </style>
    """,
    unsafe_allow_html=True
)

query = st.chat_input("💬 Ask anything about your PDFs...")


# -------------------------------
# QUESTION PROCESSING
# -------------------------------

if query:

    with st.spinner("🤖 Generating AI response..."):

        docs = retriever.invoke(query)

        context = ""

        for doc in docs:

            context += doc.page_content + "\n"


        prompt = f"""
You are a smart AI assistant that answers questions ONLY from the uploaded PDF documents.

Instructions:
- Carefully read the retrieved context.
- If the answer exists in the context, explain it clearly and confidently.
- Use simple and beginner-friendly language.
- Do NOT say "not enough information" unless the context is completely unrelated.
- Even if the information is partial, still try to answer using the available context.
- If the user makes spelling mistakes, intelligently understand the intended meaning.
- Keep answers accurate, concise, and relevant.
- Do not invent facts outside the context.

Retrieved Context:
{context}

Question:
{query}

Answer:
"""

        chat_completion = client.chat.completions.create(

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            model="llama-3.1-8b-instant",

            temperature=0.3,

            max_tokens=300
        )


        response = chat_completion.choices[0].message.content


        # SAVE CHAT HISTORY

        st.session_state.chat_history.append(
            {
                "question": query,
                "answer": response,
                "docs": docs
            }
        )


# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------

for chat in st.session_state.chat_history:

    # USER BUBBLE

    st.markdown(
        f"""
        <div style="
            background-color:#2563EB;
            padding:18px;
            border-radius:20px;
            margin-top:20px;
            margin-left:120px;
            color:white;
            box-shadow:0px 0px 10px rgba(37,99,235,0.5);
        ">

        <h4>📝 Question</h4>

        <p style="
            font-size:18px;
            line-height:1.7;
        ">
        {chat['question']}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


   
    # ANSWER BOX
    st.markdown(
        f"""
        <div style="
            background-color:#111827;
            padding:20px;
            border-radius:15px;
            margin-top:10px;
            border-left:5px solid #00FFA3;
        ">
        <h3>🤖 AI Answer</h3>
        <p style="
            font-size:18px;
            line-height:1.8;
        ">
        {chat['answer']}
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SOURCE CHUNKS
    st.markdown("### 📚 Retrieved Chunks")

    for i, doc in enumerate(chat["docs"]):

        with st.expander(
    f"📄 Chunk {i+1} - {doc.metadata.get('source', 'PDF')}"):

            st.write(doc.page_content)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        """
        <hr>
        <center>
        Built with ❤️ using Groq, LangChain, ChromaDB and Streamlit
        </center>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")

st.sidebar.subheader("About")

st.sidebar.write(
    "This chatbot uses Retrieval-Augmented Generation (RAG) "
    "to answer questions from uploaded PDF documents."
)