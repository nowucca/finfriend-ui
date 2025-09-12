# FinFriend - Personal Finance AI Assistant

FinFriend is an AI-powered personal finance assistant built with Streamlit that helps you explore and understand your financial data.

## Features

- **Quick Chat**: Get instant answers to finance questions
- **Generate Reports**: Create detailed financial reports from transaction data
- **Learning Topics**: Learn about finance concepts at your level

## Quick Start

### 1. Setup (Students - Free Access)

Get your credentials from your instructor and run:

```bash
uv run python finfriend-setup.py --username alice --pin 1234
```

This configures FinFriend to use the free aitools-llm-proxy service with the powerful `openai--gpt-oss-120b` model.

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run FinFriend

```bash
uv run streamlit run 🏠_FinFriend.py
```

## Setup Guide

For detailed setup instructions, see [SETUP.md](SETUP.md).

## Architecture

FinFriend follows a modular architecture:

- **`ui/`**: Streamlit UI components and interactions
  - `components/`: Reusable UI components (sidebar, etc.)
  - `interactions/`: UI interaction handlers (chat, etc.)
- **`services/`**: Business logic services (LLM, prompts)
- **`pages/`**: Streamlit application pages
- **`data/`**: Sample transaction datasets
- **`static/`**: Static assets (logos, etc.)

## Technology Stack

- **Streamlit**: Web application framework
- **OpenAI API**: LLM integration (compatible with aitools-llm-proxy)
- **Pandas**: Data analysis and manipulation
- **uv**: Modern Python package management

## Development

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Run with uv
uv run streamlit run 🏠_FinFriend.py
uv run python finfriend-setup.py --help
```

## License

[LICENSE](LICENSE)
