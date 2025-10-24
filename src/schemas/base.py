from pydantic import BaseModel, Field

from src.database import models


class UserInfo(BaseModel):
    id: str = Field(..., description="User ID")
    name: str = Field(..., description="User Name")
    username: str = Field(..., description="User Account Username")

    @staticmethod
    def from_model(user: models.User) -> "UserInfo":
        return UserInfo(id=user.id, name=user.name, username=user.account[0].username)


class BlobInfo(BaseModel):
    id: str = Field(..., description="Blob ID")
    filename: str = Field(..., description="Blob Filename")
    content_type: str = Field(..., description="Blob Content Type")
    url: str = Field(..., description="Blob URL")
    
    @staticmethod
    def from_model(blob: models.Blob) -> "BlobInfo":
        return BlobInfo(id=blob.id, filename=blob.filename, content_type=blob.content_type, url=blob.url)