#!/bin/bash
echo "Setting up the environment using uv..."
# Install uv if not available
if ! command -v uv &> /dev/null
then
    echo "uv could not be found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment with Python 3.8
uv venv --python 3.8

# Install dependencies using the pyproject.toml
source .venv/bin/activate
uv pip install -e .

echo "Environment setup complete! Activate with: source .venv/bin/activate"
