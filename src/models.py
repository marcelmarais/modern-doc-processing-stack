from docling.datamodel.base_models import InputFormat
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: SecretStr
    openai_api_key: SecretStr
    max_file_size: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class TokenCount(BaseModel):
    o200k_base: int
    cl100k_base: int


class ProcessDocumentResponse(BaseModel):
    markdown: str
    language: str
    mimetype: str
    token_count: TokenCount


class AcceptedMimeTypes(BaseModel):
    mime_types: dict[InputFormat, str | list[str]] = {
        InputFormat.PDF: "application/pdf",
        InputFormat.IMAGE: [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/tiff",
            "image/bmp",
            "image/webp",
        ],
        InputFormat.DOCX: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        InputFormat.HTML: "text/html",
        InputFormat.PPTX: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        InputFormat.ASCIIDOC: "text/plain",
        InputFormat.MD: "text/markdown",
        InputFormat.XLSX: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    def is_allowed_mime_type(self, mime_type: str) -> bool:
        for mime_type_entry in self.mime_types.values():
            if isinstance(mime_type_entry, list):
                if mime_type in mime_type_entry:
                    return True
            elif mime_type == mime_type_entry:
                return True
        return False

    def get_accepted_input_formats(self) -> list[InputFormat]:
        return list(self.mime_types.keys())
