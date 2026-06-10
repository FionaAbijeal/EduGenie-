def ask_pdf(message, history):
    pass

def generate_summary():
    pass

def generate_mcqs():
    pass

def generate_flashcards():
    pass
# RAG PDF CHATBOT

# =========================
# IMPORTS
# =========================

import os
import torch



from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from transformers import pipeline


# =========================
# UPLOAD PDF FILES
# =========================

print("\nUpload your PDF files...\n")



# =========================
# LOAD PDF DOCUMENTS
# =========================

all_docs = []

pdf_files = [f for f in os.listdir() if f.endswith(".pdf")]

for pdf in pdf_files:
    loader = PyPDFLoader(pdf)
    docs = loader.load()
    all_docs.extend(docs)

print(f"\nLoaded {len(all_docs)} pages from PDFs")

# =========================
# SPLIT DOCUMENTS
# =========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = splitter.split_documents(all_docs)

print(f"\nCreated {len(split_docs)} text chunks")

# =========================
# CREATE EMBEDDINGS
# =========================

print("\nCreating embeddings...\n")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# CREATE VECTOR DATABASE
# =========================

vectorstore = FAISS.from_documents(
    split_docs,
    embedding_model
)

print("\nVector database ready")

# OPTIONAL: SAVE DATABASE
vectorstore.save_local("faiss_db")

# =========================
# LOAD LANGUAGE MODEL
# =========================

print("\nLoading AI model...\n")

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto",
    torch_dtype=torch.float16
)

print("\nModel loaded successfully")

# =========================
# RAG FUNCTION
# =========================

def ask_pdf(message, history):

    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(message, k=5)

    # Combine retrieved text
    context = "\n\n".join([doc.page_content for doc in docs])

    # Prompt
    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

Do NOT make up information.

If the answer is not found in the context,
say:
"I could not find the answer in the document."

Context:
{context}

Question:
{message}

Answer:
"""

    # Generate response
    response = generator(
        prompt,
        max_new_tokens=200,
        temperature=0.3,
        do_sample=True
    )

    output = response[0]["generated_text"]

    # Extract final answer
    answer = output.split("Answer:")[-1].strip()

    return answer

def generate_summary():

    docs = vectorstore.similarity_search(
        "summary of document",
        k=10
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Summarize the following document in 5-10 bullet points.

Document:
{context}

Bullet Point Summary:
"""

    response = generator(
        prompt,
        max_new_tokens=150,
        temperature=0.1,
        do_sample=False
    )

    output = response[0]["generated_text"]

    summary = output.split("Bullet Point Summary:")[-1].strip()

    return summary

print(generate_summary())

def generate_mcqs():

    docs = vectorstore.similarity_search(
        "important topics",
        k=10
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Create 5 multiple choice questions from the document.

Format:

Q1. Question
A) Option
B) Option
C) Option
D) Option
Answer: Correct Option

Document:
{context}

MCQs:
"""

    response = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False
    )

    output = response[0]["generated_text"]

    mcqs = output.split("MCQs:")[-1].strip()

    return mcqs

print(generate_mcqs())

def generate_flashcards():

    docs = vectorstore.similarity_search(
        "important concepts",
        k=10
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Create exactly 5 flashcards.

Format:
Front: ...
Back: ...

Document:
{context}

Flashcards:
"""

    response = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False
    )

    output = response[0]["generated_text"]

    flashcards = output.split("Flashcards:")[-1].strip()

    return flashcards

print(generate_flashcards())

# =========================
# CHAT HISTORY
# =========================

chat_history = []

# =========================
# RAG FUNCTION
# =========================

def ask_pdf(message, history):

    docs = vectorstore.similarity_search(
        message,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )


    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not found in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{message}

Answer:
"""

    response = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False
    )

    output = response[0]["generated_text"]

    answer = output.split("Answer:")[-1].strip()

    # Save History
    chat_history.append({
        "question": message,
        "answer": answer
    })
    chat_history.append({
    "question": message,
    "answer": answer
})
    print("History Saved")

    return answer


# =========================
# SHOW HISTORY FUNCTION
# =========================

def show_history():

    if len(chat_history) == 0:
        print("No history found")
        return

    for i, item in enumerate(chat_history, 1):

        print(f"\n----- Chat {i} -----")

        print("Question:")
        print(item["question"])

        print("\nAnswer:")
        print(item["answer"])

        print("\n" + "="*50)


# =========================
# TEST HISTORY
# =========================

# Ask some questions first:
# ask_pdf("What is C language?", [])
# ask_pdf("What is MS Access?", [])

# Then run:
show_history()

print(chat_history)

chat_history = []

chat_history.append({
    "question": "test",
    "answer": "test answer"
})

print(chat_history)

ask_pdf("What is MS Access?", [])

print(chat_history)





















