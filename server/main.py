from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query_handler import search_documentation
import spacy

app = FastAPI()

# Allow requests from the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP model
nlp = spacy.load("en_core_web_lg")

CDP_KEYWORDS = {
    "segment": ["segment", "source", "event tracking", "analytics.js", "destination"],
    "mparticle": ["mparticle", "audience", "tracking", "user profile", "customer data"],
    "lytics": ["lytics", "customer segmentation", "audience", "unified data"],
    "zeotap": ["zeotap", "identity resolution", "data enrichment", "customer intelligence"]
}

def detect_cdp(query):
    """Uses NLP to determine which CDP the query is referring to."""
    query_lower = query.lower()
    for cdp, keywords in CDP_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            return cdp
    return "segment"  # Default to Segment if unclear

@app.get("/")
def home():
    return {"message": "Support Agent Chatbot is running!"}

@app.get("/query")
def query_docs(question: str):
    """Automatically detects CDP and searches documentation for answers."""
    detected_cdp = detect_cdp(question)
    results = search_documentation(detected_cdp, question)
    return {
        "detected_cdp": detected_cdp,
        "query": question,
        "results": results
    }

# To run: uvicorn main:app --reload
