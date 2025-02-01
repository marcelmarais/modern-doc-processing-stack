# The Modern Document Processing Stack

This is a production-ready document conversion and processing engine. It uses powerful open-source libraries to convert common file formats (PDF, DOCX, etc.) and web content to Markdown—a format that is friendly for LLMs and embedding models.

---

## Features

- **Multi-format Support**: Converts PDFs, DOCX, and more to Markdown.
- **LLM Integration**: Optionally uses a VLLM (GPT4o) via [Zerox](https://github.com/getomni-ai/zerox) for processing visually complex documents.
- **Web Content Scraping**: Converts webpages to Markdown using Jina AI Reader.
- **Metadata Extraction**: Detects document language and calculates token counts for popular tokenizers (`cl100k_base` & `o200k_base`).

---

## Requirements

- **Python**: 3.12 or higher
- **Libraries**: Refer to the [`pyproject.toml`](./pyproject.toml) file for a complete list.
- **Docker**: (Optional) For containerized deployment.

---

## Installation

### Local Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/modern-doc-processing-stack.git
    cd modern-doc-processing-stack
    ```

2.  **Create and Configure Environment Variables:**

    ```bash
    cp .env.example .env
    ```

3.  **Set Up Python Environment:**

    Use uv or your preferred environment manager. For example:

    ```bash
    uv sync
    ```

4.  **Run the Application:**

    ```bash

    uv run hypercorn src/main:app --bind 0.0.0.0:8000

    ```

### Usage example

The intention is to use this over HTTP in any other project.

```python
import os
from pathlib import Path
from typing import Any, Dict

import requests

BASE_URL = "https://your-deployed-app-url"
API_KEY = os.getenv("API_KEY", "")

def process_document(file_path: Path, use_llm: bool = False) -> Dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as file:
        files = {"file": (file_path.name, file)}
        data = {"use_llm": str(use_llm).lower()}
        response = requests.post(
            f"{BASE_URL}/process/document",
            headers={"X-API-Key": API_KEY},
            files=files,
            data=data,
        )
        response.raise_for_status()
        return response.json()

def process_url(url: str) -> Dict[str, Any]:
    response = requests.post(
        f"{BASE_URL}/process/url",
        params={"url": url},
        headers={"X-API-Key": API_KEY}
    )
    response.raise_for_status()
    return response.json()
```
