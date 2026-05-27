# AI Chatbot using Groq API

## Project Overview
This project is an AI-powered chatbot developed using Python and integrated with the Groq API. The chat system is capable of interacting with users and generating responses in real time.

## Problem Statement

The objective  was to create an AI chat system whose response could be modified by using different system prompts . The chatbot could be  used to interact with the users in real time and allowing different personalities and styles of communication to be executed in .

## Implementation

The project was developed using Python in VS Code. First, a separate virtual environment (venv) was created and activated so that all required libraries and dependencies would stay inside the project instead of affecting the system Python setup.
Groq was used to access AI models and generate an API key for authentication.

The chatbot was implemented in Python. User input is taken through the terminal, sent to the AI model using the Groq API, and the generated response is displayed back to the user interactively. System prompts and conversation history were also used to control the chatbot’s behavior and response style.

- Created a separate folder for the LLM chatbot project in VS Code
- Set up and activated a virtual environment (venv) to keep project libraries and dependencies isolated from the system Python environment
- Installed the required Groq library and generated an API key for accessing AI models
- Started by developing a basic single-turn chatbot where the AI responded to one user input at a time
- Later converted the chatbot into a multi-turn conversation system by storing message history using system, user, and assistant roles
- Added continuous user interaction using a loop so the chatbot could maintain conversations naturally
- Tested different parameters such as temperature and max tokens to improve response style and consistency


## Technologies Used
- Python
- Groq API
- Visual Studio Code (VS Code)


## Challenges Faced
- One of the challenges during development was selecting the appropriate LLM version. I      tested two different models to compare how they handled prompts, response quality, and conversational behavior before choosing the one that worked best for the chatbot.
- Faced difficulty in modifying and controlling the system response behavior correctly
- Understanding and implementing the user prompt/context handling logic required multiple iterations and testing
## Measures Taken to Resolve the Issues
- Tested two different LLM models to compare response quality and conversational behavior
- Improved response quality by refining prompts and  adjusting model parameters.
- Tested different temperature and token settings to improve response style .





## How to Run the Application

### Step 1: Clone the Repository
```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### Step 2: Navigate to the Project Directory
```bash
cd repository_name
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key
Replace the placeholder API key in the Python file with your own Groq API key.

Example:
```python
api_key = "YOUR_API_KEY"
```

### Step 5: Run the Application
```bash
python chat.py
```
## Expected Output
The chatbot accepts user input through the terminal and generates AI-based conversational responses in real time.




---

# Task 2 – RAG AI System

## Problem Worked On
Built a Retrieval-Augmented Generation (RAG) AI chatbot capable of answering questions from uploaded PDF documents instead of relying only on the model’s pre-trained knowledge.

---

## Features
- Multiple PDF support
- PDF upload support
- Semantic search using embeddings
- ChromaDB vector database
- Streamlit UI
- Chat history memory
- Source chunk display
- Persistent local database
- Logging support

---

## Technologies Used
- Python
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq API

---

## Approach
1. Loaded PDF documents using PyPDFLoader.
2. Split documents into smaller chunks using RecursiveCharacterTextSplitter.
3. Generated embeddings using the `all-MiniLM-L6-v2` embedding model.
4. Stored embeddings inside ChromaDB.
5. Converted user questions into embeddings.
6. Retrieved the most relevant chunks using semantic similarity search.
7. Passed retrieved chunks as context to the Groq LLM.
8. Generated context-aware answers from the documents.

---

## How Retrieval Works
The system converts both PDF document chunks and user questions into vector embeddings using HuggingFace embeddings. ChromaDB performs semantic similarity search to retrieve the most relevant chunks. These retrieved chunks are then passed as context to the Groq LLM, which generates accurate answers based on the uploaded document content.

---

## Issues Faced
- Incorrect chunk retrieval
- Retrieval mismatch between multiple PDFs
- HTML rendering issues in Streamlit
- Duplicate chat rendering
- Large chunk sizes reducing retrieval accuracy
- Semantic search confusion for vague queries

---

## Solutions Implemented
- Reduced chunk size for better retrieval precision
- Improved prompts to reduce hallucinations
- Added source chunk display
- Added multiple PDF support
- Added chat history memory
- Improved Streamlit UI
- Increased retrieval count for better context

---

## Possible Improvements
- Add OCR support for scanned PDFs
- Add authentication system
- Deploy application online
- Add citation highlighting
- Use advanced embedding models
- Add reranking for better retrieval accuracy

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit application:

```bash
streamlit run app.py
```

Run terminal-based RAG system:

```bash
python rag.py
```