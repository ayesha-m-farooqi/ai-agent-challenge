import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langfuse.langchain import CallbackHandler

load_dotenv()
def getHandler():
    return CallbackHandler()

def getLlm():
    return ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0,                 
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )

def invokeAgentWithTracing(chain, input_data, session_id="default_session"):
    langfuseHandler = getHandler()
    return chain.invoke(
        input_data,
        config={
            "callbacks": [langfuseHandler],
            "metadata": {"langfuse_session_id": session_id}
        }
    )

if __name__ == "__main__":
    # Example usage of invoking an agent with tracing
    llm = getLlm()
    response = invokeAgentWithTracing(llm, "What is Polmorphism in OOP java?", session_id="test_session")
    print(response.content)
