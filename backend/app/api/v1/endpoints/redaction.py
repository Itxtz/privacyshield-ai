import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.file import File

from app.services.document_service import (
    extract_text
)

from app.services.redaction_service import (
    redact_text
)

from fastapi.responses import FileResponse

from app.services.audit_service import (
    log_event
)

from app.core.security import (
    get_current_user
)

from app.models.user import User

from app.services.pdf_service import (
    create_redacted_pdf
)

from app.services.background_tasks import background_log_event

from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BadRequestException
)

from app.services.auth_service import verify_file_access

from app.core.config import settings

router = APIRouter(
    prefix="/redaction",
    tags=["Redaction"]
)


os.makedirs(
    settings.OUTPUT_DIR,
    exist_ok=True
)


@router.get("/redact/{file_id}")
def redact_document(
        file_id: int,
        background_tasks: BackgroundTasks,
        current_user: User = Depends(
            get_current_user
        ),
        db: Session = Depends(get_db)
):

    db_file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not db_file:

        raise NotFoundException(
            "File not found"
        )
    
    verify_file_access(
        db_file,
        current_user
    )

    text = extract_text(
        db_file.filepath
    )

    result = redact_text(
        text
    )

    output_filename = (
        f"redacted_{db_file.filename}"
    )

    output_path = os.path.join(
        settings.OUTPUT_DIR,
        output_filename
    )

    # Determine original file type
    extension = os.path.splitext(
        db_file.filename
    )[1].lower()

    # TXT files
    if extension == ".txt":

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                result["redacted_text"]
            )

    # PDF files
    elif extension == ".pdf":

        create_redacted_pdf(

            output_path=output_path,

            text=result["redacted_text"]
        )

    # Unsupported formats
    else:

        raise BadRequestException(
            f"Unsupported file type: {extension}"
        )
        
    background_tasks.add_task(

        background_log_event,

        user_id=current_user.id,

        action="REDACT",

        resource=db_file.filename,

        details="Document redacted"

    )

    return {

        "message": "Document redacted successfully",

        "file_id": db_file.id,

        "download_endpoint":
            f"/redaction/download/{db_file.id}",

        "summary": result["summary"]
    }

@router.get("/download/{file_id}")
def download_redacted_document(

        file_id: int,

        current_user: User = Depends(
            get_current_user
        ),

        db: Session = Depends(get_db)
):

    # Find the file in the database
    db_file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not db_file:

        raise NotFoundException(
            "File not found"
        )

    # Verify ownership
    verify_file_access(
        db_file,
        current_user
    )

    # Construct the generated redacted filename
    filename = f"redacted_{db_file.filename}"

    file_path = os.path.join(
        settings.OUTPUT_DIR,
        filename
    )

    if not os.path.exists(file_path):

        raise NotFoundException(
            "Redacted file not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )