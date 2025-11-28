"""
Router for PCOS risk assessment endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PCOSRiskRequest, PCOSRiskResponse
from app.services.pcos_service import calculate_pcos_risk

router = APIRouter(
    prefix="/pcos",
    tags=["PCOS Risk Assessment"]
)

@router.post("/risk-assessment", response_model=PCOSRiskResponse)
async def assess_pcos_risk(request: PCOSRiskRequest):
    """
    Assess PCOS risk based on reported symptoms.
    
    This endpoint calculates a risk score and provides a recommendation.
    Note: This is a heuristic assessment and NOT a medical diagnosis.
    """
    try:
        return calculate_pcos_risk(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
