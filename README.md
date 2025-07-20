# CSV Agent

Check this out in [Medium Article](https://medium.com/@wriddhirupd/csv-agent-using-mcp-with-langgraph-and-llama3-2-26652717db31)

## About the Agent
The CSV agent in this project acts as a Data Analyst that can read, describe and visualize based on the user input. Its a conversational agent that can store the older messages in its memory.

<img width="716" alt="image" src="https://github.com/user-attachments/assets/446240a1-e6bf-4574-b87e-d15cdbd80090" />

---

## Dockerized Setup (Recommended)

### Prerequisites
- [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

### 1. Build and Start Services

```sh
docker-compose up --build
```
This will start two containers:
- `ollama`: The LLM server (Ollama)
- `csv-agent`: The Python CSV agent app

### 2. Pull the Llama3.2 Model in Ollama
Before running the agent, you need to pull the model inside the Ollama container:

```sh
docker exec -it ollama ollama pull llama3.2
```

### 3. Run the Agent
Once the model is pulled, you can interact with the agent:

```sh
docker exec -it csv-agent python app/main.py
```

You can now enter your commands as usual.

---

## Prerequisites for the setup (Manual/Local):
- Install Ollama - https://ollama.com/download
- Install Python 3.12 - https://www.python.org/downloads/release/python-3120/

For this agent, we are using `Llama3.2:latest` from Ollama and connecting it through LangChain library.

## Install dependencies:
```
pip install -r requirements.txt
```

## Run:
```
python app/main.py
```
OR 
```
uv run app/main.py
```

## Results:

1. User ask: For /Users/{user}/Downloads/excel-agent-main/data.csv draw a line chart of income

---

## Notes
- The Ollama service runs on port 11434 and is required for the agent to function.
- The first time you run, pulling the model may take several minutes.
- Data and models are persisted in the `ollama-data` Docker volume.

---

## Running the Project (Step-by-Step)

### 1. Start Everything with Docker Compose

From your project root, run:

```sh
docker-compose up --build
```
- This will build the csv-agent image, start the Ollama service, and launch your agent.

### 2. **Manually Pull the Model in the Ollama Container**
Before the agent can use the model, you must pull it in the Ollama container:

```sh
docker exec -it ollama ollama pull llama3.2
```
- This is a one-time step per model/version. You only need to do this again if you want to use a new model or update an existing one.

### 3. Interact with the Agent
- The agent will start automatically and prompt you for input in the logs as soon as the model is available.
- To interact directly, you can attach to the running container:
  ```sh
  docker attach csv-agent
  ```
  or, if you want a new shell:
  ```sh
  docker exec -it csv-agent /bin/bash
  python app/main.py
  ```

### 4. Monitor Logs
To see the output and any prompts:
```sh
docker-compose logs -f csv-agent
```

### 5. Switch Models Later
- Stop the stack: `docker-compose down`
- Uncomment the desired model in `app/mcp_setup/client/stdio_client.py` (see model options in the code comments)
- Pull the new model in the Ollama container, e.g.:
  ```sh
  docker exec -it ollama ollama pull qwen3:8b
  ```
- Restart: `docker-compose up --build`

#### Example Model Options (in code):
```python
# model = ChatOllama(model="llama3.2", temperature=0)  # Llama 3.2 8B (default)
# model = ChatOllama(model="qwen3:8b", temperature=0)  # Qwen3 8B
# model = ChatOllama(model="deepseek-coder:6.7b-instruct", temperature=0)  # DeepSeek Coder 6.7B
# model = ChatOllama(model="stablelm2:12b", temperature=0)  # StableLM2 12B
```

---

## Comprehensive Quickstart: Build, Start, and Run

### 1. Build Everything (No Cache)
```sh
docker-compose build --no-cache
```

### 2. Start Ollama Service in the Background
```sh
docker-compose up -d ollama
```

### 3. Pull the Model in the Ollama Container
```sh
docker exec -it ollama ollama pull llama3.2
```

### 4. Run the Agent Interactively
```sh
docker-compose run --rm csv-agent
```
- This will give you an interactive prompt for the agent.
- You can run this command as many times as you want; the Ollama service will stay running in the background.

### 5. (Optional) Monitor Logs
```sh
docker-compose logs -f ollama
```

### 6. (Optional) Stop All Services
```sh
docker-compose down
```

---

**Summary:**
- Build with `docker-compose build --no-cache`
- Start Ollama: `docker-compose up -d ollama`
- Pull model: `docker exec -it ollama ollama pull llama3.2`
- Run agent: `docker-compose run --rm csv-agent`
- Stop all: `docker-compose down`

---

