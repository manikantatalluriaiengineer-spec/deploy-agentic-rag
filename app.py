# Streamlit Web Frontend for Agentic RAG
import streamlit as st
import requests
import json
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Agentic RAG - 100% Private",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-top: 1rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .status-online {
        background-color: #d4edda;
        color: #155724;
    }
    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Server configuration
SERVER_URL = st.sidebar.text_input(
    "Server URL",
    value="http://localhost:8000",
    help="URL of the Agentic RAG server"
)

# Check server status
@st.cache_data(ttl=10)
def check_server_health(url: str) -> bool:
    """Check if the server is running"""
    try:
        response = requests.get(f"{url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# Main UI
st.markdown('<div class="main-header">🤖 Agentic RAG System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">100% Private • Powered by Ollama & CrewAI</div>', unsafe_allow_html=True)

# Server status
is_online = check_server_health(SERVER_URL)
status_class = "status-online" if is_online else "status-offline"
status_text = "🟢 Online" if is_online else "🔴 Offline"

st.sidebar.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)

if not is_online:
    st.error(f"⚠️ Server is not running at {SERVER_URL}")
    st.info("""
    **To start the server:**
    1. Open a terminal
    2. Navigate to the project directory
    3. Run: `python3 server.py`
    """)
    st.stop()

# Query input
st.markdown("### 💬 Ask a Question")
query = st.text_area(
    "Enter your question:",
    height=100,
    placeholder="e.g., What is artificial intelligence? Explain quantum computing. What are the benefits of renewable energy?",
    help="Type your question and click 'Get Answer' to get a response from the AI agents"
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_button = st.button("🚀 Get Answer", type="primary", use_container_width=True)

# Process query
if submit_button and query:
    if not query.strip():
        st.warning("Please enter a question!")
    else:
        with st.spinner("🤔 Thinking... (This may take a minute)"):
            try:
                payload = {"query": query}
                response = requests.post(
                    f"{SERVER_URL}/predict",
                    json=payload,
                    timeout=300  # 5 minutes timeout for long responses
                )
                response.raise_for_status()
                
                result = response.json()
                answer = result.get('output', {}).get('raw', 'No response received')
                
                st.markdown("### 📝 Response")
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown(answer)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show raw JSON in expander
                with st.expander("🔍 View Raw Response"):
                    st.json(result)
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The server might be processing a complex query. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the server. Make sure the server is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# Example queries
st.markdown("---")
st.markdown("### 💡 Example Queries")
example_queries = [
    "What is artificial intelligence?",
    "Explain machine learning in simple terms",
    "What are the benefits of renewable energy?",
    "How does quantum computing work?",
    "What is the difference between Python and JavaScript?",
]

cols = st.columns(len(example_queries))
for i, example in enumerate(example_queries):
    with cols[i]:
        if st.button(f"📌 {example[:30]}...", key=f"example_{i}", use_container_width=True):
            st.session_state.query = example
            st.rerun()

# Info section
with st.expander("ℹ️ About This System"):
    st.markdown("""
    **Agentic RAG System - 100% Private**
    
    This system uses:
    - **Ollama**: Local LLM (llama3) - No API keys needed
    - **CrewAI**: Multi-agent orchestration
    - **FastAPI**: Backend server
    - **Streamlit**: Web interface
    
    **How it works:**
    1. **Researcher Agent**: Researches your query and generates insights
    2. **Writer Agent**: Synthesizes the insights into a comprehensive answer
    
    **Privacy**: Everything runs locally on your machine. No data is sent to external APIs.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🔒 100% Private • Powered by Ollama & CrewAI"
    "</div>",
    unsafe_allow_html=True
)
