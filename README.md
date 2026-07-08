# 🧠 Intelligent Tool-Orchestrating AI Assistant

An intelligent AI assistant built with **LangChain**, **Mistral AI**, and **Streamlit** that automatically decides when to use external tools to answer user queries. The assistant retrieves real-time weather information and the latest city news while demonstrating modern **LLM Tool Calling**, **Human-in-the-Loop (HITL)** approval, and **Agentic AI** workflows.

---

## ✨ Features

* 🤖 AI Agent powered by **Mistral AI**
* 🛠️ Intelligent Tool Calling with LangChain
* 🌦️ Real-time Weather using OpenWeather API
* 📰 Live News Search using Tavily Search API
* 👤 Human-in-the-Loop (HITL) Tool Approval
* 💬 Interactive Streamlit Chat Interface
* 💻 Command-Line (CLI) Version
* ⚡ Automatic Tool Selection
* 🔄 Runnable-based Agent Pipeline
* 📜 Conversation History Support
* ❌ Graceful Error Handling

---

## 🏗️ Tech Stack

**Languages**

* Python

**Frameworks & Libraries**

* LangChain
* Streamlit
* Mistral AI
* Requests
* python-dotenv
* Rich

**APIs**

* OpenWeather API
* Tavily Search API

**Concepts**

* Generative AI
* AI Agents
* Tool Calling
* Function Calling
* Runnable Pipelines
* Middleware
* Prompt Engineering
* Human-in-the-Loop (HITL)

---

## 📁 Project Structure

```text
Intelligent-Tool-Orchestrating-AI-Assistant/
│
├── app.py                  # Streamlit Web Application
├── agent.py                # Agent Logic
├── tools.py                # Weather & News Tools
├── middleware.py           # Human Approval Middleware
├── cli_agent.py           # CLI Version
├── requirements.txt
├── .env.example
├── README.md
└── assets/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/intelligent-tool-orchestrating-ai-assistant.git
cd intelligent-tool-orchestrating-ai-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
MISTRAL_API_KEY=your_mistral_api_key
OPEN_WEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

---

## ▶️ Run the CLI Version

```bash
python cli_agent.py
```

---

## 💬 Example Queries

```text
What's the weather in Delhi?

Latest news in London

Show me weather and news for Tokyo.

Is it raining in Mumbai?

Give me today's news in New York.
```

---

## 🧠 How It Works

```text
User Query
     │
     ▼
Mistral AI (LLM)
     │
     ▼
LangChain Agent
     │
     ▼
Decides Whether a Tool is Required
     │
     ├──────────────┐
     ▼              ▼
Weather Tool     News Tool
(OpenWeather)    (Tavily)
     │              │
     └──────┬───────┘
            ▼
 Tool Result Returned
            ▼
 Final AI Response
```

---

## 📸 Demo

Add screenshots or GIFs here.

Example:

```
assets/
├── home.png
├── weather.png
├── news.png
└── approval.png
```

---

## 🚀 Future Improvements

* Conversation Memory
* LangGraph Integration
* Multi-Agent Workflow
* RAG with Vector Database
* Voice Assistant
* Docker Support
* Cloud Deployment
* Additional Tool Integrations

---

## 🎯 Skills Demonstrated

* Generative AI
* LangChain Agents
* AI Tool Calling
* Function Calling
* LLM Integration
* Python
* Streamlit
* API Integration
* Middleware Design
* Runnable Pipelines
* Prompt Engineering
* Human-in-the-Loop AI

---

## ⭐ If you found this project useful

Please consider giving the repository a **Star ⭐**.

---

## 👨‍💻 Author

**Arjun Verma**

GitHub: https://github.com/yourusername
