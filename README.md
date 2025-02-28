# 📌 CDP Support Agent Chatbot
*A chatbot designed to fetch and answer questions from Customer Data Platform (CDP) documentation using NLP and web scraping.*

---

## 📖 Table of Contents
- [🚀 Features](#-features)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🔧 Running the Application](#-running-the-application)
- [📡 API Endpoints](#-api-endpoints)
- [💻 Frontend Usage](#-frontend-usage)
- [🛠 How It Works](#-how-it-works)
- [🎯 Future Improvements](#-future-improvements)
- [📜 License](#-license)

---

## 🚀 Features
✅ **Web Scraper** – Extracts documentation from CDP platforms like Segment, mParticle, Lytics, and Zeotap.  
✅ **Natural Language Processing (NLP)** – Uses `spaCy` & `fuzzywuzzy` for intelligent query handling.  
✅ **FastAPI Backend** – Provides a REST API to fetch and query documentation.  
✅ **React Frontend** – Simple chat UI that interacts with the FastAPI backend.  
✅ **Automatic CDP Detection** – Identifies the relevant CDP based on the query.  
✅ **Cross-Origin Compatibility** – Uses CORS middleware for smooth frontend-backend communication.  

---

---

## ⚙️ Installation & Setup
### 🔹 1️⃣ Clone the Repository
```bash
git clone https://github.com/onslaught7/Chat_Bot.git
```

### 🔹 2️⃣ Set Up the Backend
#### **Create & Activate Virtual Environment**
```bash
# Windows (CMD) 
cd server
python -m venv venv
venv\Scripts\activate

# macOS/Linux
cd server
python3 -m venv venv
source venv/bin/activate
```

#### **Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

#### **Download SpaCy Model**
```bash
python -m spacy download en_core_web_lg
# You  might need to the below manually, after pip install -r requirements.txt
pip install fuzzywuzzy
pip install python-Levenshtein

```

---

## 🔧 Running the Application
### 🚀 Start FastAPI Backend
```bash
uvicorn main:app --reload
```
Backend is now running at **`http://127.0.0.1:8000`**.

### 🌐 Start React Frontend
#### **Navigate to the `client/` Directory**
```bash
cd client
```

#### **Install Frontend Dependencies**
```bash
npm install
```

#### **Run the Frontend**
```bash
npm run dev
```
Frontend is now running at **`http://localhost:5173`**.

---

## 📡 API Endpoints
| Method | Endpoint           | Description |
|--------|--------------------|-------------|
| `GET`  | `/`                | Health check |
| `GET`  | `/query?question=...` | Ask a question, returns relevant documentation |

**Example Query:**  
```bash
http://127.0.0.1:8000/query?question=How do I create a user profile in mParticle?
```
**Response:**
```json
{
    "detected_cdp": "mparticle",
    "query": "How do I create a user profile in mParticle?",
    "results": [
        "To create a user profile in mParticle, go to the User Profile tab and configure attributes...",
        "Use the mParticle SDK to send identity information...",
        "For advanced setup, integrate with identity resolution features..."
    ]
}
```

---

## 💻 Frontend Usage
1. Open **`http://localhost:5173`** in your browser.  
2. Type a question like `"How do I set up a new source in Segment?"`.  
3. The bot will fetch relevant documentation and display it in the chat UI.  
4. You can continue asking more questions.  

---

## 🛠 How It Works
### 1️⃣ Web Scraper (`scraper.py`)
- Uses **Selenium & BeautifulSoup** to scrape documentation from **Segment, mParticle, Lytics, and Zeotap**.  
- Extracts useful content and stores it in the `data/` folder as `.txt` files.  

### 2️⃣ NLP-Powered Query Handling (`query_handler.py`)
- Uses **`spaCy` (`en_core_web_lg`)** for natural language understanding.  
- Uses **`fuzzywuzzy`** for fuzzy matching of questions.  
- **Filters irrelevant queries** (e.g., movies, weather).  
- Automatically **detects the relevant CDP** based on keywords.  

### 3️⃣ FastAPI Backend (`main.py`)
- Provides a **REST API** to handle frontend queries.  
- Uses **CORS middleware** to allow frontend communication.  
- Calls `query_handler.py` to return relevant answers.  

### 4️⃣ React Frontend (`client/`)
- **Simple Chat UI** where users can type questions.  
- **Sends queries to FastAPI backend** and displays responses.  
- **Supports multi-line answers** and continues conversation.  

---

## 🎯 Future Improvements
🚀 **Adding OpenAI GPT Model** for more natural responses.  
📖 **Improving Web Scraper** to handle dynamically loaded pages better.  
📊 **Adding Analytics Dashboard** to track query trends.   

---
