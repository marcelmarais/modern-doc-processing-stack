from datetime import datetime

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from pydantic import HttpUrl

from document_processing import (
    get_markdown_from_url,
    process_doc_standard,
    process_doc_with_llm,
)
from file_utils import (
    count_tokens,
    detect_language,
    get_sample_text,
    validate_uploaded_file,
)
from logger import setup_logger
from models import ProcessDocumentResponse, Settings, TokenCount

settings = Settings()  # type: ignore
logger = setup_logger(__name__)


def api_key_auth(x_api_key: str = Header(None)):
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid API key")


app = FastAPI(dependencies=[Depends(api_key_auth)])


@app.get("/", include_in_schema=False)
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "modern-doc-processing-stack",
    }


@app.post("/process/document", response_model=ProcessDocumentResponse)
async def process_document(
    file: UploadFile = File(...),
    use_llm: bool = Form(default=False),
) -> ProcessDocumentResponse:
    contents, filename, mime_type = await validate_uploaded_file(
        file=file, max_file_size=settings.max_file_size, use_llm=use_llm
    )
    if use_llm:
        markdown = await process_doc_with_llm(file_path=filename)
    else:
        markdown = await process_doc_standard(filename, contents)

    logger.info(
        f"Successfully processed document: {filename}. Detected format: {mime_type}."
    )

    language = detect_language(get_sample_text(markdown))

    await file.close()
    return ProcessDocumentResponse(
        markdown=markdown,
        language=language,
        mimetype=mime_type,
        token_count=TokenCount(
            cl100k_base=count_tokens(text=markdown, encoding_name="cl100k_base"),
            o200k_base=count_tokens(text=markdown, encoding_name="o200k_base"),
        ),
    )


@app.post("/process/url", response_model=ProcessDocumentResponse)
async def process_url(url: HttpUrl) -> ProcessDocumentResponse:
    markdown = get_markdown_from_url(url)
    if markdown is None:
        raise HTTPException(
            status_code=400, detail=f"Couldn't get markdown from URL: {url}"
        )
    language = detect_language(get_sample_text(markdown))
    return ProcessDocumentResponse(
        markdown=markdown,
        language=language,
        mimetype="text/html",
        token_count=TokenCount(
            cl100k_base=count_tokens(text=markdown, encoding_name="cl100k_base"),
            o200k_base=count_tokens(text=markdown, encoding_name="o200k_base"),
        ),
    )
