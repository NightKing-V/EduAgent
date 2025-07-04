# EduAgent
“EduAgent: AI-powered Research &amp; Exam Assistant”


| **🛠️ Layer**             | **🧰 Technology**               | **🎯 Purpose**                                  |
| ------------------------- | ------------------------------- | ----------------------------------------------- |
| **🖥️ Frontend/UI**       | Streamlit                       | Interactive web app, file upload, chat UI       |
| **🎨 UI Styling**         | HTML + Inline CSS               | Custom chat bubbles and formatting              |
| **🤖 Orchestration**      | LangChain + CrewAI              | Multi-agent workflows, chaining tasks           |
| **🧠 LLM Model**          | Mistral via Ollama              | Text generation, summarization, Q\&A            |
| **🔍 Embeddings**         | Sentence-Transformers           | Convert text to vectors for semantic search     |
| **📚 Vector Database**    | ChromaDB                        | Store and query embedded document chunks        |
| **📄 Document Parsing**   | LangChain PDF loader + chunker  | Convert PDFs to manageable text chunks          |
| **🔐 Session Management** | Streamlit session\_state + UUID | Maintain chat history and session data          |
| **🗂️ File Handling**     | OS + Temp folders               | Manage temporary uploaded files                 |
| **🚀 Deployment**         | Python 3.8+, Docker (optional)  | Run app and LLM server locally or in containers |
