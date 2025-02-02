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
