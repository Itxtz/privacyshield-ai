import os

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

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
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

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
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