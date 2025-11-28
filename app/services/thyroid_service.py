"""
Service for Thyroid Tracker logic.
"""

from typing import List, Dict
from app.models.schemas import ThyroidRiskRequest, ThyroidRiskResponse, ThyroidSymptomLog

def calculate_thyroid_risk(data: ThyroidRiskRequest) -> ThyroidRiskResponse:
    """
    Calculate thyroid risk score based on reported symptoms.
    
    This is a heuristic model and NOT a medical diagnosis.
    
    Scoring Logic:
    - Hypothyroid indicators (Weight gain, fatigue, cold, hair loss, dry skin, depression): +10 each
    - Hyperthyroid indicators (Weight loss, heat, palpitations, tremors, anxiety): +10 each
    - General/Overlap (Irregular periods, family history, neck swelling): +15 each
    
    Risk Levels:
    - 0-20: Low
    - 25-50: Moderate
    - >50: High
    """
    score = 0
    hypo_score = 0
    hyper_score = 0
    matched_symptoms = []
    
    # Hypothyroid Indicators
    if data.unexplained_weight_gain:
        score += 10
        hypo_score += 10
        matched_symptoms.append("Unexplained weight gain")
    if data.constant_fatigue:
        score += 10
        hypo_score += 5  # Overlap but leans hypo
        matched_symptoms.append("Constant fatigue")
    if data.cold_intolerance:
        score += 10
        hypo_score += 10
        matched_symptoms.append("Cold intolerance")
    if data.dry_skin:
        score += 10
        hypo_score += 10
        matched_symptoms.append("Dry skin")
    if data.hair_loss:
        score += 10
        hypo_score += 5 # Overlap
        hyper_score += 5
        matched_symptoms.append("Hair loss")
    if data.depression: # mapped from mood_changes if possible, but using general mood here
        pass 

    # Hyperthyroid Indicators
    if data.unexplained_weight_loss:
        score += 10
        hyper_score += 10
        matched_symptoms.append("Unexplained weight loss")
    if data.heat_intolerance:
        score += 10
        hyper_score += 10
        matched_symptoms.append("Heat intolerance")
    if data.palpitations:
        score += 10
        hyper_score += 10
        matched_symptoms.append("Heart palpitations")
    if data.tremors:
        score += 10
        hyper_score += 10
        matched_symptoms.append("Tremors")
        
    # General / Overlap
    if data.irregular_periods:
        score += 15
        matched_symptoms.append("Irregular periods")
    if data.family_history:
        score += 15
        matched_symptoms.append("Family history")
    if data.neck_swelling:
        score += 20
        matched_symptoms.append("Neck swelling (Goiter)")
    if data.mood_changes:
        score += 10
        matched_symptoms.append("Mood changes")

    # Determine Leaning
    if hypo_score > hyper_score:
        condition_leaning = "Hypothyroid"
    elif hyper_score > hypo_score:
        condition_leaning = "Hyperthyroid"
    else:
        condition_leaning = "Unclear"

    # Determine Risk Level
    if score <= 20:
        risk_level = "Low"
        recommendation = "Your symptoms do not strongly suggest a thyroid imbalance. Continue to monitor your health."
    elif score <= 50:
        risk_level = "Moderate"
        recommendation = f"You have some symptoms that could be related to {condition_leaning} issues. Consider tracking your symptoms for a few weeks."
    else:
        risk_level = "High"
        recommendation = f"Your symptoms strongly align with {condition_leaning} patterns. It is recommended to consult a doctor for a TSH/T3/T4 test."

    return ThyroidRiskResponse(
        risk_score=score,
        risk_level=risk_level,
        condition_leaning=condition_leaning,
        recommendation=recommendation,
        matched_symptoms=matched_symptoms
    )

def analyze_thyroid_symptoms(logs: List[ThyroidSymptomLog]) -> Dict:
    """
    Analyze a list of daily symptom logs to detect patterns.
    """
    if not logs:
        return {"status": "No data", "insights": []}
        
    insights = []
    alert_triggered = False
    
    # Calculate averages/counts
    avg_energy = sum(log.energy_level for log in logs if log.energy_level) / len(logs) if any(l.energy_level for l in logs) else 0
    high_fatigue_days = sum(1 for log in logs if log.fatigue_intensity and log.fatigue_intensity >= 4)
    temp_readings = [log.body_temperature for log in logs if log.body_temperature]
    avg_temp = sum(temp_readings) / len(temp_readings) if temp_readings else 0
    
    # Insight Logic
    if avg_energy < 4 and high_fatigue_days > len(logs) / 2:
        insights.append("You've reported consistently low energy and high fatigue. This is a common sign of Hypothyroidism.")
        alert_triggered = True
        
    if avg_temp and avg_temp < 36.1: # Celsius
        insights.append("Your average body temperature is lower than normal, which can be linked to low thyroid function.")
        
    if any(log.neck_swelling for log in logs):
        insights.append("You reported neck swelling. Please see a doctor immediately as this could be a goiter.")
        alert_triggered = True
        
    status = "Possible Thyroid Alert" if alert_triggered else "Normal"
    
    return {
        "status": status,
        "insights": insights,
        "analyzed_days": len(logs)
    }
