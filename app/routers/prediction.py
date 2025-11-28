"""
Cycle prediction API endpoints.
"""

from fastapi import APIRouter, HTTPException
import time

from app.models.schemas import (
    PredictionRequest, PredictionResponse,
    EnhancedPredictionRequest, EnhancedPredictionResponse
)
from app.services.predictor import make_prediction
from app.services.enhanced_predictor import make_enhanced_prediction
from app.ml.model_factory import get_framework_availability, get_default_framework
from app.utils.logging import log_request, log_response, log_error

router = APIRouter(prefix="/predict", tags=["Cycle Prediction"])


@router.post("", response_model=PredictionResponse)
async def predict_cycle(request: PredictionRequest):
    """
    Predict next menstrual cycle start date using PyTorch LSTM.
    
    - **past_cycles**: List of past cycle lengths in days (minimum 4 cycles)
    - **last_period_date**: Last period start date in YYYY-MM-DD format
    - **framework**: ML framework to use (only 'pytorch' is supported)
    
    Returns predicted cycle length, next period date, and confidence intervals.
    """
    start_time = time.time()
    
    try:
        log_request("/predict", "POST", f"Cycles: {len(request.past_cycles)}, Framework: {request.framework}")
        
        result = make_prediction(
            past_cycles=request.past_cycles,
            last_period_date=request.last_period_date,
            framework=request.framework
        )
        
        duration = (time.time() - start_time) * 1000
        log_response("/predict", "success", duration)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        log_error("/predict", e)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/frameworks")
async def list_frameworks():
    """List available ML frameworks for cycle prediction."""
    availability = get_framework_availability()
    default = get_default_framework()
    
    return {
        "available_frameworks": availability,
        "default": default
    }


@router.post("/enhanced", response_model=EnhancedPredictionResponse)
async def predict_cycle_enhanced(request: EnhancedPredictionRequest):
    """
    Enhanced cycle prediction with multi-feature support.
    
    Track symptoms, lifestyle factors, and flow intensity for more accurate predictions.
    
    **Features tracked:**
    - **Symptoms**: Cramps, mood changes, energy level, bloating, headaches (0-5 scale)
    - **Flow intensity**: Light, medium, or heavy
    - **Lifestyle**: Stress, exercise, sleep quality, weight changes
    
    **Returns:**
    - Predicted cycle length and next period date
    - Confidence score (0-100%) and level (low/medium/high)
    - Data quality assessment
    - Personalized health insights
    - Feature importance analysis
    
    **Example Request:**
    ```json
    {
      "cycle_records": [
        {
          "cycle_length": 28,
          "date": "2024-12-15",
          "symptoms": {"cramps": 3, "mood_changes": 2, "energy_level": 4},
          "flow_intensity": "medium",
          "lifestyle": {"stress_level": 2, "exercise_intensity": 4, "sleep_quality": 5}
        }
      ],
      "last_period_date": "2025-01-15",
      "framework": "pytorch"
    }
    ```
    """
    start_time = time.time()
    
    try:
        log_request("/predict/enhanced", "POST", f"Cycles: {len(request.cycle_records)}, Framework: {request.framework}")
        
        # Convert Pydantic models to dictionaries
        cycle_records_dict = [record.model_dump() for record in request.cycle_records]
        
        result = make_enhanced_prediction(
            cycle_records=cycle_records_dict,
            last_period_date=request.last_period_date,
            framework=request.framework
        )
        
        duration = (time.time() - start_time) * 1000
        log_response("/predict/enhanced", "success", duration)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        log_error("/predict/enhanced", e)
        raise HTTPException(status_code=500, detail=f"Enhanced prediction failed: {str(e)}")

