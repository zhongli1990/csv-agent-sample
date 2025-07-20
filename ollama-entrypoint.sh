#!/bin/sh
set -e

# Start Ollama in the background
/entrypoint.sh &

# Wait for Ollama to be ready
until curl -s http://localhost:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama to be ready..."
  sleep 2
done

echo "Ollama is ready. Pulling model..."
ollama pull llama3.2

echo "Model pull complete."

# Wait for background Ollama process
wait 