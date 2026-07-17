import os

import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.file import File as FileModel
from app.core.security import get_current_user
from app.models.user import User

from app.services.audit_service import (
    log_event
)

from fastapi import BackgroundTasks
from app.services.background_tasks import background_log_event

from app.core.config import settings

from app.core.exceptions import BadRequestException

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


os.makedirs(
    settings.UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_file(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        current_user: User = Depends(
            get_current_user
        ),
        db: Session = Depends(get_db)
):
    #Validating the file extension type
    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise BadRequestException(
            f"Only {', '.join(settings.ALLOWED_EXTENSIONS)} files are allowed."
        )
    
    #Reading the file before disk operations
    content = await file.read()

    #File Size Validation
    file_size = len(content)

    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size:
        raise BadRequestException(
            f"Maximum allowed file size is {settings.MAX_FILE_SIZE_MB} MB."
        )
    #Unique Filename Generation for DB Management
    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    db_file = FileModel(
        filename=file.filename,
        filepath=file_path,
        uploaded_by=current_user.id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    #Schedulling the log event as background task to improve user response time.
    background_tasks.add_task(

        background_log_event,

        user_id=current_user.id,

        action="UPLOAD",

        resource=db_file.filename,

        details="File uploaded"

    )

    return {
        "id": db_file.id,
        "filename": file.filename,
        "saved_to": file_path,
        "uploaded_by": current_user.email
    }