from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.risk_core import process_risk_analysis
from backend.core.security import (
    require_role
)

from backend.models.risk_audit import RiskAudit
from backend.models.return_schemas import (
    RiskResponse
)

router = APIRouter(
    prefix="/usuarios-controller",
    tags=["Usuarios Controller"]
)

# [Depends(require_role("admin", "owner")

if __name__ == '__main__':
    pass