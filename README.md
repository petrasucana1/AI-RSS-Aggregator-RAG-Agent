# 🚀 AI RSS Aggregator & RAG Agent
This project is a showcase of **low-code automation + full-code AI engineering**. It combines the best of **n8n workflows** and a **Python LangGraph-based RAG Agent** to collect, analyze, and answer questions about AI articles from multiple sources.

---

## 🌟 Project Highlights

- **n8n Workflow:** Visual, low-code automation for aggregating and filtering AI articles.  
- **Python RAG Agent:** Fully custom intelligent agent using **LangGraph, Chroma embeddings, and LLMs** to answer questions with citation.  
- **Multi-Source Aggregation:** RSS feeds from top AI websites (HackerNews, AI TechPark, KnowTechie, The Guardian, and more).  
- **Dynamic Tool Calls:** The RAG agent can make multiple tool calls to retrieve relevant info before answering.  
- **Fancy Output Ready:** Outputs can be formatted for Slack, Google Docs, Notion, or any downstream app.  

---



## 🛠 n8n Workflow (Low-Code Magic)
<img width="1446" height="556" alt="n8n-articles-workflow" src="https://github.com/user-attachments/assets/b33d1342-f0e2-4ca1-8821-d188eb1b1585" />

### ✅ What I Built:
- RSS aggregation from multiple sources.  
- Merge, Filter, and Set nodes to preprocess and structure data.  
- LLM integration (OpenAI) for selecting the **most relevant articles**.  
- Custom Code node for **structured and readable output** (Title, Author, Link, Article Text).
  
<img width="584" height="727" alt="prompt2" src="https://github.com/user-attachments/assets/8e601593-9b2b-4081-a1c2-05af11b517a9" />

### 🧠 Lessons Learned:
- Mastered multiple RSS feed integration and merging.  
- Learned to combine visual workflow nodes with LLM calls.  
- Gained experience controlling output format through code in a low-code environment.

### ⚡ Pros:
- Rapid implementation and visual clarity.  
- Easy integration with downstream apps (Slack, Docs, Notion).  
- Ideal for prototyping without heavy coding.

### ❌ Cons:
- Limited flexibility compared to custom Python code.  
- Dependency on OAuth tokens and credentials.  
- Debugging complex LLM logic is harder inside n8n nodes.

---



## 🐍 Python RAG Agent (Full-Code Power)

### ✅ What I Built:
- RSS feed parsing with `feedparser`.  
- Conversion of articles into **Documents** with metadata (link, categories).  
- **Vector store Chroma** with OpenAI embeddings (`text-embedding-3-small`).  
- **Retriever tool** for semantic search.  
- **StateGraph** loop: LLM ↔ Tool calls → iterative knowledge retrieval.  
- Answer generation with **citations to sources**.
  <img width="1571" height="656" alt="ragAgent" src="https://github.com/user-attachments/assets/e95e5cae-0708-4699-a652-6f3cf97b9f6b" />


### 🛠 Libraries & Tools:
- `langgraph` – Agent orchestration with StateGraph.  
- `langchain` & `langchain_core` – LLM integration, documents, embeddings.  
- `langchain_openai` – ChatOpenAI (`gpt-4o-mini`).  
- `langchain_chroma` – Chroma vector store for semantic search.  
- `feedparser` – RSS parsing.  
- `dotenv` – API key management.  
- Python standard libs: `os`, `typing`, `Sequence`.

### 🧠 Lessons Learned:
- Built a fully custom **RAG agent** with complete control over tool calls and conversation flow.  
- Learned semantic search & vector embeddings in action.  
- Experience in **preprocessing, deduplication, and metadata management**.  
- Integrated multiple LLM calls into a dynamic retrieval loop.

### ⚡ Pros:
- Full control over processing and output.  
- Extreme flexibility for extensions: multiple tools, LLMs, embedding types.  
- Can format outputs beautifully for Slack, Docs, Notion, etc.

### ❌ Cons:
- More time-intensive to implement & debug.  
- Complex to scale vs. low-code workflows.  
- Manual management of API keys and persistent vector data.

---
