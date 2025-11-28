from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from app.models.schemas import (
    NutritionProfileRequest, NutritionPlanResponse, DailyNutritionTip, 
    NutrientInfo, NutritionAlert, SymptomData, LifestyleData
)
from app.services.nutrition import NutritionService

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutrition"]
)

@router.post("/calculate", response_model=NutritionPlanResponse)
async def calculate_nutrition_needs(profile: NutritionProfileRequest):
    """
    Calculate daily calorie and macro requirements based on user profile.
    """
    try:
        plan = NutritionService.calculate_daily_needs(profile)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tips/{cycle_day}", response_model=DailyNutritionTip)
async def get_daily_tips(
    cycle_day: int, 
    cycle_length: int = Query(28, ge=20, le=45, description="Average cycle length")
):
    """
    Get nutrition tips based on the current day of the menstrual cycle.
    """
    try:
        tips = NutritionService.get_phase_nutrition(cycle_day, cycle_length)
        return tips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/essentials", response_model=List[NutrientInfo])
async def get_essential_nutrients():
    """
    Get a list of essential nutrients for women's health.
    """
    return NutritionService.get_essential_nutrients()

@router.post("/alerts", response_model=List[NutritionAlert])
async def generate_nutrition_alerts(
    symptoms: SymptomData = Body(..., description="Current symptoms"),
    lifestyle: LifestyleData = Body(..., description="Current lifestyle factors")
):
    """
    Generate personalized nutrition alerts based on symptoms and lifestyle data.
    """
    try:
        alerts = NutritionService.generate_alerts(symptoms, lifestyle)
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
