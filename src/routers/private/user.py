from typing import Annotated, List
from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from src.database import models
from src.dependencies.auth import get_current_user
from src.dependencies.basic import get_db
from src.schemas import base
from src.utils.s3 import upload_local_to_s3, save_upload_files_locally

router = APIRouter()


@router.post("/blob", response_model=base.BlobInfo)
async def upload_image(
        user: Annotated[models.User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        file: UploadFile,
):
    uploaded_files = save_upload_files_locally(file)
    url = upload_local_to_s3(
        uploaded_files[0].path,
        f"user/{str(uuid4())}.{uploaded_files[0].extension}",
        file.content_type
    )

    new_blob = models.Blob(
        id=str(uuid4()),
        filename=file.filename,
        content_type=file.content_type,
        url=url
    )

    db.add(new_blob)
    db.flush()
    user.blobs.append(new_blob)

    db.commit()

    return base.BlobInfo.from_model(new_blob)


@router.get('/blobs', response_model=List[base.BlobInfo])
async def get_user_blobs(
        user: Annotated[models.User, Depends(get_current_user)]
):
    return [base.BlobInfo.from_model(blob) for blob in user.blobs]
