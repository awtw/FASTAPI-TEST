from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def lazy_relationship(*args, **kwargs):
    return relationship(*args, uselist=True, **kwargs)

user_blob_association = Table(
    "user_chatrooms",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("blob_id", String(36), ForeignKey("blobs.id"), primary_key=True),
)