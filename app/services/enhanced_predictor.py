"""
Enhanced menstrual cycle prediction service.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np
from fastapi import HTTPException

from app.services.predictor import make_prediction

def make_enhanced_prediction(
    cycle_records: List[Dict[str, Any]], 
    last_period_date: str, 
    framework: str = "pytorch"
) -> Dict[str, Any]:
    """
    Make enhanced prediction using multi-feature data.
    
    Args:
        cycle_records: List of cycle records with symptoms and lifestyle data
        last_period_date: Last period start date (YYYY-MM-DD)
        framework: ML framework to use
        
    Returns:
        Dictionary matching EnhancedPredictionResponse schema
    """
    try:
        # Extract cycle lengths from records
        past_cycles = [record['cycle_length'] for record in cycle_records]
        
        # Get base prediction
        base_result = make_prediction(
            past_cycles=past_cycles,
            last_period_date=last_period_date,
            framework=framework
        )
        
        # Calculate enhanced metrics
        # Note: These are simplified calculations since feature_engineering 
        # and confidence modules are currently empty.
        
        # Calculate confidence score based on consistency
        std_dev = base_result['statistics']['std_deviation']
        cycle_count = len(past_cycles)
        
        # Base confidence starts at 70%
        confidence_score = 70.0
        
        # Adjust based on consistency (lower std dev is better)
        if std_dev < 2.0:
            confidence_score += 15
        elif std_dev < 4.0:
            confidence_score += 5
        elif std_dev > 6.0:
            confidence_score -= 10
            
        # Adjust based on history length
        if cycle_count > 10:
            confidence_score += 10
        elif cycle_count > 6:
            confidence_score += 5
            
        # Cap at 99%
        confidence_score = min(99.0, max(10.0, confidence_score))
        
        # Determine confidence level
        if confidence_score >= 80:
            confidence_level = "high"
        elif confidence_score >= 60:
            confidence_level = "medium"
        else:
            confidence_level = "low"
            
        # Generate basic insights
        insights = []
        avg_length = base_result['statistics']['average_cycle_length']
        
        if avg_length < 26:
            insights.append("Your cycle is shorter than average.")
        elif avg_length > 32:
            insights.append("Your cycle is longer than average.")
        else:
            insights.append("Your cycle length is within the normal range.")
            
        if std_dev > 5:
            insights.append("Your cycle length varies significantly.")
        else:
            insights.append("Your cycle is quite regular.")
            
        # Analyze symptoms if available
        symptom_count = sum(1 for r in cycle_records if r.get('symptoms'))
        if symptom_count > 0:
            insights.append(f"You have tracked symptoms for {symptom_count} cycles.")
            
        return {
            **base_result,
            "confidence_score": round(confidence_score, 1),
            "confidence_level": confidence_level,
            "data_quality": "good" if cycle_count >= 6 else "fair",
            "insights": insights,
            "feature_importance": {
                "cycle_history": 0.8,
                "symptoms": 0.1,
                "lifestyle": 0.1
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced prediction failed: {str(e)}")
