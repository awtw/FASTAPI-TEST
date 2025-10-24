from pydantic import BaseModel, Field


class TextOnly(BaseModel):
    text: str = Field(..., title="Text", description="Text content")


class Token(BaseModel):
    access_token: str = Field(default='example_token')
    token_type: str = Field(default='bearer')


class UploadedFile(BaseModel):
    path: str = Field(..., title="Local Path")
    original_file_name: str = Field(..., title="Original File Name")
    extension: str = Field(..., title="File Extension")
    content_type: str = Field(..., title="Content Type")
