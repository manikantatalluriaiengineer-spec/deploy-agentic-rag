# Private Agentic RAG System

A fully private, enterprise-ready AI agent system that runs entirely on-premises using local LLMs. No external API dependencies, no data leaves your infrastructure, and complete control over your AI workflows.

## 🎯 Overview

This system implements a multi-agent RAG (Retrieval-Augmented Generation) architecture using CrewAI for agent orchestration and Ollama for local LLM inference. It provides a production-ready API, web interface, and CLI client for seamless integration into your workflows.

## ✨ Key Features

- **🔒 100% Private & Secure**: All processing happens locally - no data transmission to external services
- **💰 Zero API Costs**: No usage fees, subscription costs, or rate limits
- **🤖 Multi-Agent Architecture**: Specialized agents (Researcher + Writer) collaborate for comprehensive answers
- **🌐 Multiple Interfaces**: Web UI, REST API, and CLI client for different use cases
- **⚙️ Fully Customizable**: Easy to modify agents, prompts, and workflows
- **🚀 Production Ready**: FastAPI backend with health checks and error handling

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │ (Web UI / CLI / API)
└──────┬──────┘
       │
┌──────▼──────────┐
│  FastAPI Server │
└──────┬──────────┘
       │
┌──────▼──────────┐
│   CrewAI Crew   │
│  ┌───────────┐  │
│  │ Researcher│  │ → Analyzes query & generates insights
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │   Writer  │  │ → Synthesizes comprehensive answer
│  └───────────┘  │
└──────┬──────────┘
       │
┌──────▼──────┐
│   Ollama    │ (Local LLM - llama3)
└─────────────┘
```

## 📋 Prerequisites

- **Python 3.11+**
- **Ollama** installed and running ([Download](https://ollama.com))
- At least one Ollama model installed (e.g., `llama3`, `qwen3`, `mistral`)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install crewai crewai-tools litellm fastapi uvicorn streamlit
```

### 2. Setup Ollama

Ensure Ollama is installed and running:

```bash
# Check Ollama installation
ollama --version

# Pull a model (if not already installed)
ollama pull llama3

# Verify model is available
ollama list
```

### 3. Start the Backend Server

```bash
python3 server.py
```

The server will start on `http://localhost:8000`. You should see:
```
🚀 Starting 100% Private Agentic RAG Server...
📡 Server running on http://localhost:8000
💡 Using local Ollama model: llama3
🔒 No API keys required - 100% private!
```

### 4. Access the Web Interface

In a new terminal:

```bash
streamlit run app.py
```

Open your browser to: **http://localhost:8501**

### 5. Use the CLI Client (Optional)

```bash
python3 client.py --query "What is artificial intelligence?"
```

## 📁 Project Structure

```
deploy-agentic-rag/
├── server.py          # FastAPI backend server
├── app.py             # Streamlit web frontend
├── client.py          # Command-line client
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔧 Configuration

### Changing the LLM Model

Edit `server.py` and modify the model name:

```python
# Change from llama3 to your preferred model
llm = LLM(model="ollama/qwen3")  # or "ollama/mistral", etc.
```

### Customizing Agents

Modify agent roles, goals, and backstories in `server.py`:

```python
researcher_agent = Agent(
    role="Your Custom Role",
    goal="Your custom goal",
    backstory="Your custom backstory",
    ...
)
```

## 🌐 API Documentation

### Health Check

```bash
GET http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

### Query Endpoint

```bash
POST http://localhost:8000/predict
Content-Type: application/json

{
  "query": "Your question here"
}
```

Response:
```json
{
  "output": {
    "raw": "Comprehensive answer to your question..."
  }
}
```

### Example with cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

## 💻 Usage Examples

### Web Interface

1. Start the server: `python3 server.py`
2. Start the frontend: `streamlit run app.py`
3. Open browser to `http://localhost:8501`
4. Enter your question and click "Get Answer"

### CLI Client

```bash
# Single query
python3 client.py --query "What is quantum computing?"

# Multiple queries
python3 client.py --query "Explain microservices architecture"
python3 client.py --query "What are the benefits of cloud computing?"
```

### API Integration

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"query": "What is artificial intelligence?"}
)

result = response.json()
print(result["output"]["raw"])
```

## 🔍 How It Works

1. **User Query**: Question is received via web UI, CLI, or API
2. **Researcher Agent**: Analyzes the query, understands the context, and generates research insights
3. **Writer Agent**: Takes the research insights and synthesizes them into a comprehensive, well-structured answer
4. **Response**: Final answer is returned to the user

Both agents use the local Ollama LLM for processing, ensuring complete privacy and no external dependencies.

## 🎯 Use Cases

- **Internal Knowledge Base**: Answer questions about company documentation
- **Technical Support**: Provide technical explanations and troubleshooting
- **Research Assistant**: Help with research and analysis tasks
- **Educational Tool**: Explain complex concepts in simple terms
- **Privacy-Sensitive Applications**: Where data cannot leave the organization

## 🔒 Security & Privacy

- **No External API Calls**: All processing happens locally
- **No Data Transmission**: Your queries never leave your infrastructure
- **No API Keys Required**: No external service dependencies
- **On-Premises Deployment**: Full control over your data and infrastructure

## ⚡ Performance Considerations

- **Response Time**: 30-60 seconds per query (depends on hardware and model size)
- **Hardware Requirements**: 
  - Minimum: 8GB RAM, modern CPU
  - Recommended: 16GB+ RAM, GPU for faster inference
- **Model Selection**: Larger models provide better answers but require more resources

## 🛠️ Troubleshooting

### Server Won't Start

```bash
# Check if port 8000 is in use
lsof -ti:8000

# Kill process on port 8000 if needed
lsof -ti:8000 | xargs kill -9
```

### Ollama Not Responding

```bash
# Check if Ollama is running
pgrep -f ollama

# Restart Ollama
pkill ollama
ollama serve &
```

### Model Not Found

```bash
# List available models
ollama list

# Pull a model
ollama pull llama3
```

### Dependencies Missing

```bash
# Reinstall dependencies
pip install --upgrade crewai crewai-tools litellm fastapi uvicorn streamlit
```

## 📚 Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **Ollama**: Local LLM inference engine
- **FastAPI**: Modern Python web framework for APIs
- **Streamlit**: Rapid web app development
- **LiteLLM**: LLM abstraction layer

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for use and modification.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/crewAIInc/crewAI) for the agent framework
- [Ollama](https://ollama.com) for local LLM support
- [FastAPI](https://fastapi.tiangolo.com) for the API framework
- [Streamlit](https://streamlit.io) for the web interface

---

**Built with ❤️ for privacy-first AI applications**
