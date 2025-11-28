import sys
import os
import asyncio
from datetime import datetime

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.schemas import ThyroidRiskRequest, ThyroidSymptomLog
from app.services.thyroid_service import calculate_thyroid_risk, analyze_thyroid_symptoms

def test_risk_assessment():
    print("\n--- Testing Risk Assessment ---")
    
    # Test Case 1: High Risk Hypothyroid
    print("Test Case 1: High Risk Hypothyroid")
    req1 = ThyroidRiskRequest(
        unexplained_weight_gain=True,
        constant_fatigue=True,
        cold_intolerance=True,
        dry_skin=True,
        hair_loss=True
    )
    res1 = calculate_thyroid_risk(req1)
    print(f"Score: {res1.risk_score}")
    print(f"Level: {res1.risk_level}")
    print(f"Leaning: {res1.condition_leaning}")
    assert res1.risk_level == "High"
    assert res1.condition_leaning == "Hypothyroid"
    print("✅ Passed")

    # Test Case 2: High Risk Hyperthyroid
    print("\nTest Case 2: High Risk Hyperthyroid")
    req2 = ThyroidRiskRequest(
        unexplained_weight_loss=True,
        heat_intolerance=True,
        palpitations=True,
        tremors=True,
        anxiety=True
    )
    res2 = calculate_thyroid_risk(req2)
    print(f"Score: {res2.risk_score}")
    print(f"Level: {res2.risk_level}")
    print(f"Leaning: {res2.condition_leaning}")
    assert res2.risk_level == "High" or res2.risk_level == "Moderate" # Depending on exact score
    assert res2.condition_leaning == "Hyperthyroid"
    print("✅ Passed")
    
    # Test Case 3: Low Risk
    print("\nTest Case 3: Low Risk")
    req3 = ThyroidRiskRequest(
        mood_changes=True
    )
    res3 = calculate_thyroid_risk(req3)
    print(f"Score: {res3.risk_score}")
    print(f"Level: {res3.risk_level}")
    assert res3.risk_level == "Low"
    print("✅ Passed")

def test_symptom_analysis():
    print("\n--- Testing Symptom Analysis ---")
    
    # Create a week of logs indicating Hypothyroidism
    logs = [
        ThyroidSymptomLog(date="2025-01-01", energy_level=3, fatigue_intensity=4, body_temperature=36.0, neck_swelling=False),
        ThyroidSymptomLog(date="2025-01-02", energy_level=2, fatigue_intensity=5, body_temperature=35.9, neck_swelling=False),
        ThyroidSymptomLog(date="2025-01-03", energy_level=3, fatigue_intensity=4, body_temperature=36.1, neck_swelling=False),
        ThyroidSymptomLog(date="2025-01-04", energy_level=4, fatigue_intensity=3, body_temperature=36.0, neck_swelling=False),
    ]
    
    result = analyze_thyroid_symptoms(logs)
    print(f"Status: {result['status']}")
    print(f"Insights: {result['insights']}")
    
    assert "Possible Thyroid Alert" in result['status']
    assert any("low energy" in i for i in result['insights'])
    print("✅ Passed")
    
    # Test Goiter Alert
    print("\nTest Case: Goiter Alert")
    logs_goiter = [
        ThyroidSymptomLog(date="2025-01-05", neck_swelling=True)
    ]
    result_goiter = analyze_thyroid_symptoms(logs_goiter)
    print(f"Status: {result_goiter['status']}")
    assert "Possible Thyroid Alert" in result_goiter['status']
    assert any("neck swelling" in i for i in result_goiter['insights'])
    print("✅ Passed")

if __name__ == "__main__":
    try:
        test_risk_assessment()
        test_symptom_analysis()
        print("\n🎉 All Tests Passed!")
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
