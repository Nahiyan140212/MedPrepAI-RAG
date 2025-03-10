# MedPrepAI: RAG-Based Medical Chatbot for USMLE Step 1

## Overview

MedPrepAI is an advanced chatbot designed for medical students preparing for the **USMLE Step 1**. It leverages **Retrieval-Augmented Generation (RAG)** to provide accurate and up-to-date answers from the **First Aid for the USMLE Step 1 2024** guide. 

## Features

- **Context-Aware Responses**: Uses RAG to retrieve and generate precise answers.
- **Medical Knowledge Base**: Trained on **First Aid for the USMLE Step 1 2024**.
- **Conversational Interface**: User-friendly chat experience.
- **Customizable Knowledge Base**: Easily update or expand the dataset.

## Tech

- **Python** (FastAPI for backend)
- **LangChain** (RAG-based retrieval)
- **OpenAI API** (LLM for response generation)
- **Pinecone** (Vector database for efficient retrieval)
- **HTML, CSS** (Frontend UI)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/MedPrepAI-RAG.git
cd MedPrepAI-RAG
```
### 2. Create a virtual environment
``` bash
conda create -n medprepai python=3.10 -y
conda activate medprepai

```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.Configure API Keys
create a .env file and add the keys
```bash 
OPENAI_API_KEY="your_openai_api_key"
PINECONE_API_KEY="your_pinecone_api_key"
```
### 4. Prepare the Knowledge Base
```bash
python store_index.py

```

### 5. Run the chatbot
```bash
python app.py

```
### 6. Access UI
```bash
http://localhost:8000
```
