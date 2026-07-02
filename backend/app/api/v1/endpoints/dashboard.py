from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.dashboard_service import (
    get_dashboard_summary
)

from app.services.dashboard_service import (
    risk_distribution
)

from app.core.security import (
    require_admin
)
from app.core.security import (
    get_current_user
)
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(

    current_user: User = Depends(
        require_admin
    ),

    db: Session = Depends(get_db)
):

    return get_dashboard_summary(db)

@router.get("/risk-distribution")
def get_risk_distribution(

        current_user: User = Depends(require_admin),

        db: Session = Depends(get_db)
):

    return risk_distribution(db)