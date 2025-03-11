import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt

app = FastAPI()

# Load environment variables - for GCP, these will come from environment variables
# set in your Cloud Run configuration
load_dotenv()  # Still useful for local development

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY or OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize global variables for reuse across requests
embeddings = None
rag_chain = None

@app.on_event("startup")
async def startup_event():
    """Initialize resources when the application starts."""
    global embeddings, rag_chain
    
    try:
        embeddings = download_hugging_face_embeddings()
        index_name = "medprep"
        docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        llm = OpenAI(temperature=0.4, max_tokens=500)
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        print("RAG chain initialized successfully")
    except Exception as e:
        print(f"Failed to initialize RAG chain: {e}")
        raise

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse("chat.html", {"request": request})
    except Exception as e:
        return HTMLResponse(content=f"Error loading template: {str(e)}", status_code=500)

@app.post("/get")
async def chat(msg: str = Form(...)):
    try:
        if not rag_chain:
            return "Error: System not initialized properly"
        
        response = rag_chain.invoke({"input": msg})
        return response.get("answer", "Error: No answer found")
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Health check endpoint for GCP
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get the port from the environment variable
    port = int(os.getenv("PORT", 8080))
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)