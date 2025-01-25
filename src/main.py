from datetime import datetime
from io import BytesIO
from fastapi import FastAPI, File, Form, UploadFile
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling_core.types.io import DocumentStream
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from file_utils import count_tokens, get_sample_text, validate_uploaded_file
from logger import setup_logger
from models import AcceptedMimeTypes, ProcessDocumentResponse, Settings, TokenCount
from langdetect import detect, LangDetectException


app = FastAPI()

logger = setup_logger(__name__)
settings = Settings()

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


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "modern-doc-processing-stack",
    }


@app.post("/process-document", response_model=ProcessDocumentResponse)
async def process_document(
    file: UploadFile = File(...), use_llm: bool = Form(default=False)
) -> ProcessDocumentResponse:
    filename, contents = await validate_uploaded_file(file, settings.max_file_size)
    await file.close()

    converter_result = converter.convert(
        DocumentStream(name=filename, stream=BytesIO(contents))
    )

    origin = converter_result.document.origin
    num_pages = len(converter_result.document.pages)
    mimetype = origin.mimetype if origin else "unknown"

    logger.info(
        f"Successfully processed document: {filename}. Detected format: {mimetype}. Number of pages: {num_pages}"
    )

    markdown_text = converter_result.document.export_to_markdown()

    try:
        language = detect(get_sample_text(markdown_text))
        logger.info(f"Detected language: {language}")
    except LangDetectException as e:
        logger.warning(f"Could not detect language: {e}")
        language = "unknown"

    return ProcessDocumentResponse(
        markdown=markdown_text,
        language=language,
        mimetype=mimetype,
        token_count=TokenCount(
            cl100k_base=count_tokens(text=markdown_text, encoding_name="cl100k_base"),
            o200k_base=count_tokens(text=markdown_text, encoding_name="o200k_base"),
        ),
    )
