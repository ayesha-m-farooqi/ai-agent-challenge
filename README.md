# AI Agent Challenge – Sandbox Pipeline

##  Overview
This project implements a sandbox AI agent pipeline for citizen risk detection.  
It integrates **Groq LLMs** with **Langfuse tracing** to produce flagged outputs and a valid Session ID for submission.

##  Project Structure
├── data/                # Input datasets (CSV + JSON)
├── src/
│   ├── preprocessing.py # Step 1: Merge & clean data
│   ├── agent_logic.py   # Step 2: Risk rules
│   ├── groq_integration.py # Step 3: Groq + Langfuse logging
│   └── main.py          # Step 4: Pipeline runner
├── output/
│   └── output.txt       # Flagged citizen IDs
└── README.md

Code

##  Setup
1. Clone the repo:
  ```bash
  git clone https://github.com/ayesha-m-farooqi/ai-agent-challenge.git
  cd ai-agent-challenge
  ```
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Create a .env file with keys:
  ```code
  GROQ_API_KEY=your_groq_key_here
  LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
  LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
  ```
## Running the Pipeline
1. Preprocessing
  ```bash
  python src/preprocessing.py # Produces merged dataframe.
  ```
2. Agent Logic
  ```bash
  python src/agent_logic.py # Flags risky citizens.
  ```
3. Integration + Tracing
  ```bash
  python src/groq_integration.py # Runs Groq model and logs trace in Langfuse and prints Session ID.
  ```
4. Final Submission
  ```bash
  python src/main.py # Writes flagged IDs to output/output.txt.
  ```
## Submission
Include:
1. output/output.txt
2. .zip of repo
3. Langfuse Session ID
