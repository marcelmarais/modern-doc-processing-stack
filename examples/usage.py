import os
from pathlib import Path

import requests
from pydantic import BaseModel

BASE_URL = "https://your-api-url.com"
API_KEY = os.getenv("API_KEY", "")


class TokenCount(BaseModel):
    o200k_base: int
    cl100k_base: int


class ProcessDocumentResponse(BaseModel):
    markdown: str
    language: str
    mimetype: str
    token_count: TokenCount


def process_document(file_path: Path, use_llm: bool = False) -> ProcessDocumentResponse:
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
        return ProcessDocumentResponse(**response.json())


def process_url(url: str) -> ProcessDocumentResponse:
    response = requests.post(
        f"{BASE_URL}/process/url", params={"url": url}, headers={"X-API-Key": API_KEY}
    )
    response.raise_for_status()
    return ProcessDocumentResponse(**response.json())
