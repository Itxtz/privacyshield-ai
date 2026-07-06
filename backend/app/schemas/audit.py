from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):

    id: int

    user_id: int

    username: str

    action: str

    resource: str

    details: str | None = None

    timestamp: datetime

    class Config:
        from_attributes = True