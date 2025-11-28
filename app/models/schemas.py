"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chatbot interaction."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chatbot interaction."""
    response: str
    safety_triggered: Optional[bool] = False


class PredictionRequest(BaseModel):
    """Request model for cycle prediction."""
    past_cycles: List[int] = Field(
        ...,
        description="List of past menstrual cycle lengths in days",
        example=[28, 30, 27, 29, 28, 31, 28, 29, 27, 30, 28, 29]
    )
    last_period_date: str = Field(
        ...,
        description="Last period start date in YYYY-MM-DD format",
        example="2025-01-15"
    )
    framework: Optional[str] = Field(
        default="pytorch",
        description="ML framework to use (only 'pytorch' is supported)",
        example="pytorch"
    )
    
    @field_validator('past_cycles')
    @classmethod
    def validate_cycles(cls, v):
        """Validate cycle lengths are reasonable."""
        if len(v) < 4:
            raise ValueError('Need at least 4 past cycles for prediction')
        if any(c < 20 or c > 45 for c in v):
            raise ValueError('Cycle lengths must be between 20 and 45 days')
        return v
    
    @field_validator('last_period_date')
    @classmethod
    def validate_date(cls, v):
        """Validate date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @field_validator('framework')
    @classmethod
    def validate_framework(cls, v):
        """Validate framework choice."""
        if v != 'pytorch':
            raise ValueError('Only "pytorch" framework is supported')
        return v


class PredictionResponse(BaseModel):
    """Response model for cycle prediction."""
    predicted_cycle_length: int = Field(..., description="Predicted next cycle length in days")
    predicted_next_period: str = Field(..., description="Predicted next period start date (YYYY-MM-DD)")
    predicted_next_period_formatted: str = Field(..., description="Predicted date in readable format")
    confidence_interval: dict = Field(..., description="Confidence interval for prediction")
    statistics: dict = Field(..., description="Historical cycle statistics")
    uncertainty_days: float = Field(..., description="Prediction uncertainty in days")
    framework_used: str = Field(..., description="ML framework used for prediction")


# ============================================================================
# Enhanced Multi-Feature Prediction Models
# ============================================================================

class SymptomData(BaseModel):
    """Symptom tracking data for a cycle."""
    cramps: Optional[int] = Field(None, ge=0, le=5, description="Cramp intensity (0=none, 5=severe)")
    mood_changes: Optional[int] = Field(None, ge=0, le=5, description="Mood changes (0=none, 5=severe)")
    energy_level: Optional[int] = Field(None, ge=0, le=5, description="Energy level (0=very low, 5=very high)")
    bloating: Optional[int] = Field(None, ge=0, le=5, description="Bloating (0=none, 5=severe)")
    headaches: Optional[int] = Field(None, ge=0, le=5, description="Headaches (0=none, 5=severe)")


class LifestyleData(BaseModel):
    """Lifestyle factors for a cycle."""
    stress_level: Optional[int] = Field(None, ge=0, le=5, description="Stress level (0=none, 5=very high)")
    exercise_intensity: Optional[int] = Field(None, ge=0, le=5, description="Exercise intensity (0=none, 5=very intense)")
    sleep_quality: Optional[int] = Field(None, ge=0, le=5, description="Sleep quality (0=very poor, 5=excellent)")
    weight_change: Optional[int] = Field(None, ge=-2, le=2, description="Weight change (-2=significant loss, 0=stable, 2=significant gain)")


class CycleRecord(BaseModel):
    """Complete cycle record with all features."""
    cycle_length: int = Field(..., ge=20, le=45, description="Cycle length in days")
    date: str = Field(..., description="Period start date (YYYY-MM-DD)")
    symptoms: Optional[SymptomData] = Field(None, description="Symptom data for this cycle")
    flow_intensity: Optional[str] = Field(None, description="Flow intensity: light, medium, or heavy")
    lifestyle: Optional[LifestyleData] = Field(None, description="Lifestyle factors for this cycle")
    
    @field_validator('flow_intensity')
    @classmethod
    def validate_flow(cls, v):
        """Validate flow intensity."""
        if v is not None and v.lower() not in ['light', 'medium', 'heavy']:
            raise ValueError('Flow intensity must be: light, medium, or heavy')
        return v.lower() if v else None
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        """Validate date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v


class EnhancedPredictionRequest(BaseModel):
    """Enhanced prediction request with multi-feature support."""
    cycle_records: List[CycleRecord] = Field(
        ...,
        min_length=4,
        description="List of cycle records with symptoms and lifestyle data"
    )
    last_period_date: str = Field(
        ...,
        description="Last period start date in YYYY-MM-DD format",
        example="2025-01-15"
    )
    framework: Optional[str] = Field(
        default="pytorch",
        description="ML framework to use (only 'pytorch' is supported)",
        example="pytorch"
    )
    
    @field_validator('last_period_date')
    @classmethod
    def validate_date(cls, v):
        """Validate date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @field_validator('framework')
    @classmethod
    def validate_framework(cls, v):
        """Validate framework choice."""
        if v != 'pytorch':
            raise ValueError('Only "pytorch" framework is supported')
        return v


class EnhancedPredictionResponse(BaseModel):
    """Enhanced prediction response with confidence and insights."""
    predicted_cycle_length: int = Field(..., description="Predicted next cycle length in days")
    predicted_next_period: str = Field(..., description="Predicted next period start date (YYYY-MM-DD)")
    predicted_next_period_formatted: str = Field(..., description="Predicted date in readable format")
    confidence_interval: dict = Field(..., description="Confidence interval for prediction")
    statistics: dict = Field(..., description="Historical cycle statistics")
    uncertainty_days: float = Field(..., description="Prediction uncertainty in days")
    framework_used: str = Field(..., description="ML framework used for prediction")
    
    # Enhanced fields
    confidence_score: float = Field(..., ge=0, le=100, description="Prediction confidence score (0-100%)")
    confidence_level: str = Field(..., description="Confidence level: low, medium, high")
    data_quality: str = Field(..., description="Data quality assessment")
    insights: List[str] = Field(..., description="Personalized health insights")
    feature_importance: Optional[dict] = Field(None, description="Importance of each feature in prediction")


# ============================================================================
# PCOS Risk Assessment Models
# ============================================================================

class PCOSRiskRequest(BaseModel):
    """Request model for PCOS risk assessment."""
    irregular_periods: bool = Field(..., description="Do you have irregular periods?")
    weight_gain: bool = Field(..., description="Have you experienced unexplained weight gain?")
    excess_hair_growth: bool = Field(..., description="Do you have excess hair growth (hirsutism)?")
    acne: bool = Field(..., description="Do you have severe acne?")
    family_history: bool = Field(..., description="Does anyone in your family have PCOS?")
    dark_skin_patches: bool = Field(..., description="Do you have dark patches of skin?")
    cycle_length_avg: Optional[int] = Field(None, description="Average cycle length in days")


class PCOSRiskResponse(BaseModel):
    """Response model for PCOS risk assessment."""
    risk_score: int = Field(..., description="Calculated risk score (0-100)")
    risk_level: str = Field(..., description="Risk level: Low, Moderate, High")
    recommendation: str = Field(..., description="Health recommendation based on risk")

