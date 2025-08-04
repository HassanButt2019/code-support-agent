# 🧠 Developer Support Agent

An AI-powered assistant that helps developers explore and understand large codebases by answering natural language questions with accurate file paths, line numbers, and contextual explanations.

This project uses **LangChain**, **ChromaDB**, and **OpenAI** to build a smart code search and reasoning system, backed by **Retrieval-Augmented Generation (RAG)**.

---

## 🚀 Features

## ✅ Completed Features

- 🔍 **Natural Language Q&A**  
  Ask questions like _"Where is the database connection initialized?"_

- 📂 **Python Code Ingestion**  
  Parses your codebase using `ast` and chunks by function or class for context-aware retrieval.

- 🔗 **Source Linking**  
  Returns file path and line numbers with GitHub-style links to the exact code location.

- ⚙️ **FastAPI Backend**  
  Provides `/ask` and `/ingest` endpoints for integration.

- 🔐 **JWT Authentication**  
  Login support with Bearer tokens to enable multi-user functionality.

- 📎 **Dynamic GitHub Ingestion**  
  Accepts public GitHub repo URL at runtime and ingests it dynamically.

- 🧠 **LangChain-Powered Search**  
  Uses OpenAI embeddings and Chroma vector DB for semantic document retrieval.

---

## 🚧 Planned / Upcoming Features

- 🧠 Function-aware metadata filtering (e.g., only search `auth.py`)
- 🧩 Hybrid search: combine keyword and embedding-based ranking
- 📊 Snippet preview in response (first 2–5 lines of matched chunk)
- 🔁 Reranking with Cohere/BGE models for higher relevance
- 🧭 Mermaid.js/Graphviz-based Navigation Graphs
- 🌍 Multi-language support via [Tree-sitter](https://tree-sitter.github.io/)
- 🧵 Conversation memory for follow-up developer questions
- 🔄 Diff Agent to compare branches/commits
- 🕵️ Paste stack trace → get root cause explanation
- 🛡️ Security scan mode for vulnerable patterns like `eval()`
- 🧰 Workspace upload: zip or repo ingestion from frontend
- 🧠 VSCode-like inline AI assistant (Chrome extension)
- 📄 Downloadable API/Code Summary Reports
- ⏱️ Token-limited ingestion with repo/file limits
- 🧹 Storage optimization: auto-cleanup, LRU eviction, or per-user quotas

---

## 📦 Installation & Usage

```bash
git clone https://github.com/your-org/dev-support-agent.git
cd dev-support-agent
pip install -r requirements.txt
uvicorn app.main:app --reload

---

## 🧪 Example Question & Response

**Q:** "Where is the greet function defined?"

```json
{
  "answer": "The greet function is defined at the top of the file, outside any class.",
  "sources": [
    {
      "file": "data/hello.py",
      "lines": "1-2",
      "github_url": "https://github.com/your-org/your-repo/blob/main/hello.py#L1-L2"
    }
  ]
}


🧠 Sample Questions You Can Ask
Here are some useful and real-world developer queries you can ask the agent after ingesting a GitHub repo like portfolio_backend:

✅ General Architecture & Setup
"Where is the FastAPI app initialized?"

"Which file defines the database connection?"

"Where is the base route (/) defined?"

"What is the purpose of config.py?"

✅ API Endpoints
"What are the available project-related endpoints?"

"Where is the /projects POST route implemented?"

"Where is the route for deleting a project by ID?"

"What does the /projects/{id} GET route return?"

✅ Models & Schemas
"Where is the SQLAlchemy model for a project defined?"

"What fields are included in the Project schema?"

"Which schema is used for project creation?"

✅ Error Handling / Validation
"Where is input validation performed in the /projects route?"

"How does the app handle project not found errors?"

✅ Utilities & Config
"Where are environment variables loaded and used?"

"How is the database URI constructed?"

"What logging configuration is used (if any)?"

✅ Advanced / Logic-Focused
"How does the app filter projects by ID?"

"How is data committed to the database?"

"How is SQLAlchemy session handled?"

"How are models and schemas connected in the response flow?"

✅ Bonus: Meta Questions
"What does this project do overall?"

"How could you extend this app to support user authentication?"

"Which parts of the code can be reused across microservices?"