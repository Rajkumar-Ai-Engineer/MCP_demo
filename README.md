# MCP Based Agent Orchestration

A web application demonstrating agent orchestration using the Model Context Protocol, featuring a Python backend, HTML front-end templates, and containerized deployment support.

---

## Overview

This project implements an orchestration system powered by the Model Context Protocol. It coordinates intelligent agents to handle tasks, connect tools, and expose an interactive web interface.

Key highlights:

* Python backend serving agent logic and MCP integrations via `app.py`
* Web user interface powered by templates
* Modular source layout organized inside `src`
* Containerized setup via `Dockerfile` for consistent deployment across environments

---

## Project Structure

```text
MCP_demo/
├── src/                  # Core orchestration logic, agent definitions, and utilities
├── templates/            # HTML front-end templates for the web interface
├── .gitignore            # Git ignore rules
├── app.py                # Main application entry point and server startup
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── setup.py              # Package installation and metadata
└── README.md             # Project documentation

```

---

## Prerequisites

* Python 3.10 or higher
* pip package manager
* Docker, if deploying inside a container
* Valid API keys for the underlying LLM provider, such as Anthropic, OpenAI, or Google AI

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rajkumar-Ai-Engineer/MCP_demo.git
cd MCP_demo

```

### 2. Set up a virtual environment

```bash
python -m venv venv

```

Activate the environment:

* On Linux or macOS:

```bash
source venv/bin/activate

```

* On Windows:

```bash
venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

If installing in development mode:

```bash
pip install -e .

```

### 4. Configure environment variables

Create an `.env` file in the root directory and define the required credentials:

```bash
# Provider API keys
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key

# Application settings
PORT=5000
HOST=0.0.0.0
DEBUG=True

```

---

## Running the Application

### Local execution

Start the server using `app.py`:

```bash
python app.py

```

Open a browser and navigate to:

```text
http://localhost:5000

```

---

## Docker Deployment

To build and run the application as a Docker container:

### 1. Build the image

```bash
docker build -t mcp-demo .

```

### 2. Run the container

```bash
docker run -d -p 5000:5000 --env-file .env --name mcp-demo-container mcp-demo

```

Access the service at `http://localhost:5000`.

---

## Core Components

* **MCP Client and Server Integration:** Coordinates agent execution loops, tool registrations, and protocol communication.
* **Agent Engine:** Manages prompt routing, tool invocation, and multi-turn message handling inside `src/`.
* **Web UI:** Renders views from `templates/` to submit prompts, inspect agent traces, and monitor tool outputs in real time.
