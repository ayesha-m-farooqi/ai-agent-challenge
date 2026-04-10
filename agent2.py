import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_openai_functions_agent
from langchain_classic.agents import AgentExecutor
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langfuse import get_client
import csv

# Initialize Langfuse tracing early so spans are recorded for the agent and tool execution.
# Requires LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_HOST to be set in the environment.
# Example on Windows PowerShell:
#   setx LANGFUSE_PUBLIC_KEY "pk-lf-..."
#   setx LANGFUSE_SECRET_KEY "sk-lf-..."
#   setx LANGFUSE_HOST "https://cloud.langfuse.com"

def init_langfuse_client():
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    host = os.environ.get("LANGFUSE_HOST")

    if not public_key or not secret_key or not host:
        raise EnvironmentError(
            "Langfuse tracing requires LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_HOST."
        )

    return get_client(public_key=public_key)

client = init_langfuse_client()

# Use Groq client via OpenAI SDK
# client = OpenAI(
#     base_url="https://api.groq.com/openai/v1",
#     api_key=os.environ.get("GROQ_API_KEY")
# )

# Wrap Groq in LangChain's ChatOpenAI interface
llm = ChatOpenAI(
    model="moonshotai/kimi-k2-instruct-0905",
    temperature=0,
    api_key="API_KEY",
    base_url="https://api.groq.com/openai/v1",
)

# Define a simple tool and trace it as a Langfuse tool observation.
@client.observe(name="fake_search", as_type="tool")
def fake_search(query: str) -> str:
    """Pretend to search the web."""
    return f"Pretend search results for: {query}"

fake_search_tool = tool(fake_search)

# System prompt
system_prompt = "You are StudyBuddy, a helpful AI agent for coding and exam prep."

# Memory setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# Build prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent
agent = create_openai_functions_agent(
    llm=llm,
    tools=[fake_search_tool],
    prompt=prompt
)

# Add executor (this is what you call) - now executing with memory
agent_executor = AgentExecutor(agent=agent, tools=[fake_search_tool], memory=memory, verbose=True)

@client.observe(name="studybuddy_agent_execution", as_type="agent")
def run_agent(input_text: str):
    return agent_executor.invoke({"input": input_text})


def main():
    print(run_agent("Explain polymorphism in OOP with Java?"))
    print(run_agent("can you explain encapsulation?"))


if __name__ == "__main__":
    main()
