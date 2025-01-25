from fastapi import HTTPException, UploadFile, status
import magic
import tiktoken
from logger import setup_logger
from models import AcceptedMimeTypes


logger = setup_logger(__name__)


async def validate_uploaded_file(
    file: UploadFile, max_file_size: int
) -> tuple[str, bytes]:
    filename, size = file.filename, file.size
    if not size:
        logger.error("File size is missing")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size is missing",
        )
    if size > max_file_size:
        logger.error(
            f"File size {size} exceeds the maximum allowed size of {max_file_size}"
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size {size} exceeds the maximum allowed size of {max_file_size}",
        )
    if not filename:
        logger.warning("File name is missing. Setting to 'Document'")
        filename = "Document"

    contents = await file.read()
    content_type_from_content = magic.from_buffer(contents, mime=True)
    logger.info(f"Content type from content: {content_type_from_content}")

    if not AcceptedMimeTypes().is_allowed_mime_type(content_type_from_content):
        logger.error(f"Content type {content_type_from_content} is not allowed")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported media type: {content_type_from_content}",
        )

    return filename, contents


def get_sample_text(text: str, max_chars: int = 3000) -> str:
    """
    Get a sample of text for language detection.
    Takes the first few paragraphs up to max_chars, ensuring we don't cut words.
    """
    if len(text) <= max_chars:
        return text

    # Find the last space before max_chars to avoid cutting words
    last_space = text.rfind(" ", 0, max_chars)
    if last_space == -1:
        return text[:max_chars]
    return text[:last_space]


def count_tokens(text: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))
