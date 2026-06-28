from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.file import File

from app.models.analysis import (
    AnalysisResult
)

from app.services.document_service import (
    extract_text
)

from app.services.pii_service import (
    detect_pii
)

from app.services.risk_service import (
    calculate_risk
)

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get("/analyze/{file_id}")
def analyze_document(
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

    findings = detect_pii(text)

    risk = calculate_risk(
        findings
    )

    analysis = AnalysisResult(

        file_id=file_id,

        risk_score=risk["score"],

        risk_level=risk["level"],

        findings_count=len(findings)
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return {

        "analysis_id": analysis.id,

        "file_id": file_id,

        "filename": db_file.filename,

        "findings_count": len(findings),

        "risk_score": risk["score"],

        "risk_level": risk["level"],

        "reasons": risk["reasons"],

        "findings": findings
    }

@router.get("/history")
def get_analysis_history(
        current_user: User = Depends(
            get_current_user
        ),
        db: Session = Depends(get_db)
):

    results = (

        db.query(
            AnalysisResult,
            File
        )

        .join(
            File,
            AnalysisResult.file_id == File.id
        )

        .filter(
            File.uploaded_by == current_user.id
        )

        .all()

    )

    history = []

    for analysis, file in results:

        history.append({

            "analysis_id": analysis.id,

            "filename": file.filename,

            "risk_score": analysis.risk_score,

            "risk_level": analysis.risk_level,

            "findings_count": analysis.findings_count,

            "created_at": analysis.created_at

        })

    return history