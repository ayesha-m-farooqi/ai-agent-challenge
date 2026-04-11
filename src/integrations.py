import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langfuse.langchain import CallbackHandler

load_dotenv()

langfuseHandler = CallbackHandler()

def getLlm():
    return ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0,                 
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )

def invokeAgentWithTracing(chain, input_data):
    return chain.invoke(
        input_data,
        config={"callbacks": [langfuseHandler]}
    )

if __name__ == "__main__":
    
    llm = getLlm()
    response = invokeAgentWithTracing(llm, "What is the current health status of the system?")
    print(response)
