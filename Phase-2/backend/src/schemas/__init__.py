"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Base error response schema."""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred"
            }
        }
