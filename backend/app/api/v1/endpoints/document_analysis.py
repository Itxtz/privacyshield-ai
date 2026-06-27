from fastapi import APIRouter

from app.services.document_service import (
    extract_text
)

from app.services.pii_service import (
    detect_pii
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/analyze/{file_id}")
def analyze_document(
        file_id: int
):

    file_path = f"uploads/sample.txt"

    text = extract_text(
        file_path
    )

    findings = detect_pii(text)

    return {
        "file_id": file_id,
        "findings": findings
    }