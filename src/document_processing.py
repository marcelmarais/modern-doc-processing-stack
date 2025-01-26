from io import BytesIO
from typing import Optional

import requests  # type: ignore
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling_core.types.io import DocumentStream
from pydantic import HttpUrl
from pyzerox import zerox  # type: ignore

from logger import setup_logger
from models import AcceptedMimeTypes

logger = setup_logger(__name__)


async def process_doc_with_llm(file_path: str) -> str:
    result = await zerox(file_path=file_path)

    return "\n\n".join([page.content for page in result.pages])


async def process_doc_standard(filename: str, contents: bytes) -> str:
    converter = DocumentConverter(
        allowed_formats=AcceptedMimeTypes().get_accepted_input_formats(),
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend
            ),
            InputFormat.DOCX: WordFormatOption(
                pipeline_cls=SimplePipeline,
            ),
        },
    )

    converter_result = converter.convert(
        DocumentStream(name=filename, stream=BytesIO(contents))
    )

    return converter_result.document.export_to_markdown()


def get_markdown_from_url(url: HttpUrl) -> Optional[str]:
    jina_ai_prefix = "https://r.jina.ai/"
    markdown_url = jina_ai_prefix + str(url)
    markdown = requests.get(markdown_url)
    if markdown.status_code != 200:
        logger.error(f"Couldn't get markdown from URL: {markdown_url}")
        return None

    split_markdown = markdown.text.split("Markdown Content:")
    if len(split_markdown) < 2:
        logger.error(f"Couldn't clean markdown for URL: {markdown_url}")
        return None

    clean_markdown = split_markdown[1].strip()
    return clean_markdown
