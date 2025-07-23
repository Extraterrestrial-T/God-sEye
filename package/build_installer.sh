#!/usr/bin/env bash
# Ensure Ollama is installed and gemma:3n is pulled
echo "Checking Ollama model..."
ollama pull gemma:3n || exit 1

# Create standalone executable
pyinstaller --onefile main.py --add-data "assets/snapshots:assets/snapshots"