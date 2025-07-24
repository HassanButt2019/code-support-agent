# 🧠 Developer Support Agent

An AI-powered assistant that helps developers explore and understand large codebases by answering natural language questions with accurate file paths, line numbers, and contextual explanations.

This project uses **LangChain**, **ChromaDB**, and **OpenAI** to build a smart code search and reasoning system, backed by **Retrieval-Augmented Generation (RAG)**.

---

## 🚀 Features

✅ Already Implemented:
- 🔍 Ask natural language questions about your codebase
- 📂 Ingest Python code and chunk by function/class using `ast`
- 🔗 Respond with file paths and line numbers
- 📎 Auto-generate GitHub-style links for referenced code chunks
- 🧠 FastAPI backend with `/ask` endpoint

🛠️ Planned/Upcoming Features:
- 🧠 **Function-aware metadata filtering** (e.g., only search `auth.py`)
- 🧩 **Hybrid search**: combine keyword and embedding-based search
- 📊 **Code snippet preview** in API response
- 🔁 **Reranking** with Cohere/BGE models for higher relevance
- 🧭 **Navigation Graphs** using Mermaid.js or Graphviz
- 🌍 **Multi-language support** (JavaScript, Java, etc. using Tree-sitter)
- 🧵 **Conversation memory** for follow-up developer questions
- 🔄 **Diff Agent** to compare two branches or versions
- 🕵️ **Error Trace Explainer**: paste stack trace → get probable cause
- 🛡️ **Security scan mode**: find unsafe patterns like `eval`
- 🧰 **Workspace upload**: support `.zip` upload or GitHub repo fetch
- 🧠 **VSCode-like inline assistant** (future browser plugin)
- 📄 **Downloadable project summary reports** (e.g., API routes)

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