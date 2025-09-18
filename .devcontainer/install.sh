#!/bin/bash

DEV_PATH="/workspaces/$(basename $(pwd))/.devcontainer"
MODEL_FILE="/workspaces/$(basename $(pwd))/qwen2.5-0.5b-instruct-q2_k.gguf"

# Check if model file already exists
if [ -f "$MODEL_FILE" ]; then
    echo "✅ Model already exists, skipping setup."
    exit 0
fi

# Optionally remove copilot
# rm -rf ~/.vscode-remote/extensions/github.copilot* && chmod -w ~/.vscode-remote/extensions

# Ensure devcontainer path exists
mkdir -p "$DEV_PATH"

# Set environment variables if not already in .bashrc
BASHRC="$HOME/.bashrc"
grep -qxF "export LLAMA_CPP_LIB_PATH=$DEV_PATH" "$BASHRC" || echo "export LLAMA_CPP_LIB_PATH=$DEV_PATH" >> "$BASHRC"
grep -qxF "export LD_LIBRARY_PATH=$DEV_PATH:\$LD_LIBRARY_PATH" "$BASHRC" || echo "export LD_LIBRARY_PATH=$DEV_PATH:\$LD_LIBRARY_PATH" >> "$BASHRC"

export LLAMA_CPP_LIB_PATH=$DEV_PATH
export LLAMA_CPP_LIB="$DEV_PATH/libllama.so"
export LD_LIBRARY_PATH=$DEV_PATH:$LD_LIBRARY_PATH

# Install Python package
echo "⏳ Installing inference engine (llama-cpp-python)..."
export CMAKE_ARGS="-DLLAMA_BUILD=OFF"
pip install -q --upgrade pip
pip install -q llama-cpp-python==0.3.10
echo "✅ Inference engine installed."

# Download model
echo "⏳ Downloading model..."
wget -q -O "$MODEL_FILE" https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q2_k.gguf
echo "✅ Model downloaded."

echo ""
echo "✅ DevContainer setup complete! You can now start working on your assignment."
