# 100% Private Agentic RAG using Ollama (local LLM)
# Simple FastAPI version - No API keys required!

from crewai import Crew, Agent, Task, LLM
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Use local Ollama model (using llama3 which is already installed)
llm = LLM(model="ollama/llama3")

# Initialize agents
researcher_agent = Agent(
    role="Research Specialist",
    goal="Accurately research and understand the user's specific question, then provide detailed insights and facts about the topic",
    backstory="You are an expert researcher with deep knowledge across many fields. You carefully analyze questions and provide accurate, factual information. You focus on understanding exactly what the user is asking and provide relevant information about that specific topic.",
    verbose=True,
    tools=[],  # 100% local (no API keys needed)
    llm=llm,
    allow_delegation=False
)

writer_agent = Agent(
    role="Technical Writer",
    goal="Write a clear, accurate, and comprehensive answer that directly addresses the user's question",
    backstory="You are a skilled technical writer who creates clear, accurate explanations. You take research insights and synthesize them into well-structured answers that directly answer what the user asked. You ensure the answer is relevant to the specific question asked.",
    verbose=True,
    llm=llm,
    allow_delegation=False
)

researcher_task = Task(
    description="""Carefully analyze the user's question: "{query}"

Your task is to:
1. Understand exactly what the user is asking about
2. Research and gather accurate information about that specific topic
3. Provide detailed insights and facts related to the user's question
4. Focus ONLY on the topic mentioned in the query - do not confuse it with other topics

User's question: {query}""",
    expected_output="A detailed research report with accurate facts and insights about the specific topic mentioned in the user's question",
    agent=researcher_agent,
)

writer_task = Task(
    description="""Using the research insights provided, write a comprehensive answer to the user's question: "{query}"

Requirements:
1. Directly answer the user's specific question
2. Use the research insights to provide accurate information
3. Ensure your answer is about the exact topic the user asked about
4. Write clearly and comprehensively
5. Do not confuse the topic with other unrelated subjects

User's question: {query}""",
    expected_output="A clear, accurate, and comprehensive answer that directly addresses the user's specific question",
    agent=writer_agent,
)

crew = Crew(
    agents=[researcher_agent, writer_agent],
    tasks=[researcher_task, writer_task],
    verbose=True,
)

# FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/predict")
async def predict(request: QueryRequest):
    try:
        result = crew.kickoff(inputs={"query": request.query})
        return JSONResponse(content={"output": {"raw": str(result)}})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting 100% Private Agentic RAG Server...")
    print("📡 Server running on http://localhost:8000")
    print("💡 Using local Ollama model: llama3")
    print("🔒 No API keys required - 100% private!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
