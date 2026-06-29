import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
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

router = APIRouter(
    prefix="/redaction",
    tags=["Redaction"]
)

OUTPUT_DIR = "redacted_documents"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


@router.get("/redact/{file_id}")
def redact_document(
        file_id: int,
        db: Session = Depends(get_db)
):

    db_file = db.query(File).filter(
        File.id == file_id
    ).first()

    if not db_file:

        raise HTTPException(
            status_code=404,
            detail="File not found"
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
        OUTPUT_DIR,
        output_filename
    )

    with open(
            output_path,
            "w",
            encoding="utf-8"
    ) as f:

        f.write(
            result["redacted_text"]
        )

    return {

        "original_file": db_file.filename,

        "redacted_file": output_filename,

        "output_path": output_path,

        "summary": result["summary"],

        "redacted_text":
            result["redacted_text"]
    }

@router.get("/download/{filename}")
def download_redacted_document(
        filename: str
):

    file_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )