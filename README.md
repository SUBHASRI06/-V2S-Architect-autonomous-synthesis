⚡ V2S Architect – Autonomous Vision-to-System Synthesis Engine

V2S Architect is a research-grade prototype that transforms hand-drawn hardware architecture sketches into structured blueprints and production-ready hardware code repositories using Large Language Models.

It enables a full end-to-end pipeline:

Sketch → Blueprint Extraction → Code Generation → Repository Packaging

Built using Streamlit and Gemini 2.5 Flash.

🚀 Overview

V2S Architect demonstrates an autonomous synthesis pipeline capable of:

Interpreting uploaded architectural diagrams

Extracting structured system blueprints (JSON + Mermaid graph)

Generating multi-file hardware code (e.g., Verilog modules) and software code(e.g., Python,Java,SQL)

Automatically packaging output into a production-ready repository

Providing downloadable ZIP artifacts

This project showcases LLM-driven system design automation.

🧠 System Architecture

The pipeline operates in three main phases:

1️⃣ Blueprint Extraction

Accepts image input (PNG/JPG)

Uses Gemini Vision model

Converts diagram into structured JSON representation

Generates Mermaid diagram for visualization

2️⃣ Code Synthesis

Streams multi-file hardware code generation

Uses structured prompts based on extracted blueprint

Automatically parses file markers

Generates separate source files

3️⃣ Production Packaging

Saves generated files to structured output directory

Auto-generates project README

Creates downloadable ZIP package

🖥️ Tech Stack

Python

Streamlit (UI framework)

Gemini 2.5 Flash (Vision + Code Generation)

dotenv (API key management)

Regex-based file parsing

JSON blueprint extraction

Mermaid graph generation

📂 Project Structure
V2S_ARCHITECT/
│
├── app.py              # Streamlit UI + pipeline orchestration
├── agents.py           # V2SAgent (Gemini interaction layer)
├── utils1.py           # File saving & ZIP packaging utilities
├── requirements.txt    # Dependencies
├── README.md
└── .gitignore

⚙️ Installation

Clone the repository:

git clone https://github.com/SUBHASRI06/-V2S-Architect-autonomous-synthesis.git
cd -V2S-Architect-autonomous-synthesis


Create virtual environment (recommended):

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

🔑 Environment Setup

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here


Do NOT commit .env to version control.

▶️ Running the Application
streamlit run app.py


Then open in browser:

http://localhost:8501

📦 Usage Workflow

Upload hand-drawn or digital architecture sketch

Click “Execute Synthesis Pipeline”

Wait for blueprint extraction and code generation

Download production-ready ZIP package

📊 Features

Vision-driven blueprint extraction

Streaming code generation

Multi-file project synthesis

Automatic repository packaging

Live workspace visualization

Custom dark professional UI theme

Structured state management

🧪 Current Status

This project is a research prototype demonstrating autonomous system synthesis capabilities.

It is not intended for production deployment but showcases:

LLM orchestration

Prompt engineering

Agent abstraction

Automated repository generation

Vision-to-code workflow

🎯 Key Highlights

End-to-end automation from visual architecture to code

Modular agent-based design

Clean UI with real-time streaming output

Secure API key handling

Structured output generation

🚧 Future Improvements

Multi-language synthesis (SystemVerilog, VHDL, C++)

Validation of generated hardware modules

Diagram-to-netlist conversion

Cloud deployment

Multi-agent collaborative architecture refinement

Evaluation benchmarking

📌 Potential Applications

Rapid hardware prototyping

Educational hardware labs

Automated design assistants

AI-assisted FPGA workflows

Research in autonomous code synthesis

🛡 Security Note

API keys are stored locally using .env.
Ensure .env is added to .gitignore.

👩‍💻 Author

Developed as an exploration into autonomous LLM-driven hardware synthesis systems.

⭐ If You Found This Interesting

Star the repository and feel free to fork or experiment.
