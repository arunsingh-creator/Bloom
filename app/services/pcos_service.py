"""
Service for PCOS risk assessment logic.
"""

from app.models.schemas import PCOSRiskRequest, PCOSRiskResponse

def calculate_pcos_risk(data: PCOSRiskRequest) -> PCOSRiskResponse:
    """
    Calculate PCOS risk score based on reported symptoms.
    
    This is a heuristic model and NOT a medical diagnosis.
    
    Scoring Logic:
    - Irregular periods: 30 points
    - Excess hair growth: 20 points
    - Acne: 10 points
    - Weight gain: 15 points
    - Family history: 15 points
    - Dark skin patches: 10 points
    
    Risk Levels:
    - 0-30: Low
    - 35-60: Moderate
    - >60: High
    """
    score = 0
    
    if data.irregular_periods:
        score += 30
    if data.excess_hair_growth:
        score += 20
    if data.weight_gain:
        score += 15
    if data.family_history:
        score += 15
    if data.acne:
        score += 10
    if data.dark_skin_patches:
        score += 10
        
    # Additional check for cycle length if provided
    if data.cycle_length_avg:
        if data.cycle_length_avg > 35 or data.cycle_length_avg < 21:
            # If they didn't already say irregular periods, add points
            if not data.irregular_periods:
                score += 20
                
    # Determine risk level
    if score <= 30:
        risk_level = "Low"
        recommendation = "Your symptoms do not strongly suggest PCOS. Maintain a healthy lifestyle and track your cycles."
    elif score <= 60:
        risk_level = "Moderate"
        recommendation = "You have some symptoms associated with PCOS. Consider monitoring your symptoms and consulting a doctor if they persist."
    else:
        risk_level = "High"
        recommendation = "Your reported symptoms are strongly associated with PCOS. It is highly recommended to consult a healthcare provider for a proper evaluation."
        
    return PCOSRiskResponse(
        risk_score=score,
        risk_level=risk_level,
        recommendation=recommendation
    )
