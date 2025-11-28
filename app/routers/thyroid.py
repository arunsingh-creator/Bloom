"""
Router for Thyroid Tracker endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.models.schemas import ThyroidRiskRequest, ThyroidRiskResponse, ThyroidSymptomLog
from app.services.thyroid_service import calculate_thyroid_risk, analyze_thyroid_symptoms

router = APIRouter(
    prefix="/thyroid",
    tags=["Thyroid Tracker"]
)

@router.post("/risk-assessment", response_model=ThyroidRiskResponse)
async def assess_thyroid_risk(request: ThyroidRiskRequest):
    """
    Assess Thyroid risk based on reported symptoms.
    
    This endpoint calculates a risk score and provides a recommendation.
    Note: This is a heuristic assessment and NOT a medical diagnosis.
    """
    try:
        return calculate_thyroid_risk(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=Dict)
async def analyze_thyroid_logs(logs: List[ThyroidSymptomLog]):
    """
    Analyze a list of daily symptom logs to detect thyroid patterns.
    
    Returns:
    - Status (Normal / Possible Thyroid Alert)
    - Insights based on data
    """
    try:
        return analyze_thyroid_symptoms(logs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
