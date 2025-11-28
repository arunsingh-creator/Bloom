"""
Menstrual cycle prediction service.
"""

from typing import List
from datetime import datetime, timedelta
import numpy as np
from fastapi import HTTPException

from app.ml.preprocessing import preprocess_data, denormalize, calculate_uncertainty
from app.ml.model_factory import train_model, predict, get_framework_availability


def make_prediction(past_cycles: List[int], last_period_date: str, framework: str) -> dict:
    """
    Core prediction logic that trains model and generates predictions.
    
    Args:
        past_cycles: List of past cycle lengths in days
        last_period_date: Last period start date (YYYY-MM-DD)
        framework: ML framework to use (must be 'pytorch')
        
    Returns:
        Dictionary with prediction results
        
    Raises:
        HTTPException: If PyTorch is not available or prediction fails
    """
    # Validate PyTorch availability
    availability = get_framework_availability()
    
    if framework != 'pytorch':
        raise HTTPException(
            status_code=400,
            detail="Only PyTorch framework is supported. Please use framework='pytorch'"
        )
    
    if not availability['pytorch']:
        raise HTTPException(
            status_code=500,
            detail="PyTorch is not installed. Please install: pip install torch"
        )
    
    # Preprocess data
    SEQUENCE_LENGTH = 6
    X, y, min_val, max_val, seq_len = preprocess_data(past_cycles, SEQUENCE_LENGTH)
    
    # Train model
    model = train_model(framework, X, y)
    
    # Prepare last sequence for prediction
    last_sequence = np.array(past_cycles[-seq_len:], dtype=np.float32)
    last_sequence_normalized = (
        (last_sequence - min_val) / (max_val - min_val)
        if max_val != min_val
        else np.ones_like(last_sequence) * 0.5
    )
    
    # Make prediction
    predicted_normalized = predict(framework, model, last_sequence_normalized)
    
    # Denormalize prediction
    predicted_cycle_length = denormalize(predicted_normalized, min_val, max_val)
    predicted_cycle_length = int(round(predicted_cycle_length))
    
    # Calculate next period date
    last_date = datetime.strptime(last_period_date, "%Y-%m-%d")
    next_period_date = last_date + timedelta(days=predicted_cycle_length)
    
    # Calculate uncertainty
    uncertainty = calculate_uncertainty(past_cycles)
    earliest_date = next_period_date - timedelta(days=int(uncertainty))
    latest_date = next_period_date + timedelta(days=int(uncertainty))
    
    # Compile response
    return {
        "predicted_cycle_length": predicted_cycle_length,
        "predicted_next_period": next_period_date.strftime('%Y-%m-%d'),
        "predicted_next_period_formatted": next_period_date.strftime('%A, %B %d, %Y'),
        "confidence_interval": {
            "predicted_days": predicted_cycle_length,
            "min_days": predicted_cycle_length - int(uncertainty),
            "max_days": predicted_cycle_length + int(uncertainty),
            "earliest_date": earliest_date.strftime('%Y-%m-%d'),
            "latest_date": latest_date.strftime('%Y-%m-%d')
        },
        "statistics": {
            "average_cycle_length": float(np.mean(past_cycles)),
            "std_deviation": float(np.std(past_cycles)),
            "min_cycle": int(min(past_cycles)),
            "max_cycle": int(max(past_cycles)),
            "total_cycles_analyzed": len(past_cycles)
        },
        "uncertainty_days": float(uncertainty),
        "framework_used": framework
    }
