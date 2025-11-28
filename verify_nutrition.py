import sys
import os
sys.path.append(os.getcwd())

from app.services.nutrition import NutritionService
from app.models.schemas import NutritionProfileRequest, NutritionGoal, ActivityLevel, SymptomData, LifestyleData

def test_nutrition_calculator():
    print("\n--- Testing Nutrition Calculator ---")
    profile = NutritionProfileRequest(
        age=25,
        height=165,
        weight=60,
        activity_level=ActivityLevel.MODERATE,
        goal=NutritionGoal.MAINTAIN
    )
    plan = NutritionService.calculate_daily_needs(profile)
    print(f"Profile: {profile}")
    print(f"Plan: {plan}")
    
    assert plan.calories > 1200
    assert plan.protein > 0
    assert plan.water_intake > 0
    print("✅ Calculator Test Passed")

def test_phase_tips():
    print("\n--- Testing Phase Tips ---")
    # Menstrual
    tip1 = NutritionService.get_phase_nutrition(cycle_day=2)
    print(f"Day 2 (Menstrual): {tip1.focus}")
    assert "Iron" in tip1.focus
    
    # Follicular
    tip2 = NutritionService.get_phase_nutrition(cycle_day=10)
    print(f"Day 10 (Follicular): {tip2.focus}")
    assert "Energy" in tip2.focus
    
    # Ovulation
    tip3 = NutritionService.get_phase_nutrition(cycle_day=14)
    print(f"Day 14 (Ovulation): {tip3.focus}")
    assert "Protein" in tip3.focus
    
    # Luteal
    tip4 = NutritionService.get_phase_nutrition(cycle_day=25)
    print(f"Day 25 (Luteal): {tip4.focus}")
    assert "Bloating" in tip4.focus
    
    print("✅ Phase Tips Test Passed")

def test_alerts():
    print("\n--- Testing Alerts ---")
    symptoms = SymptomData(energy_level=2, bloating=4)
    lifestyle = LifestyleData(stress_level=5)
    
    alerts = NutritionService.generate_alerts(symptoms, lifestyle)
    for alert in alerts:
        print(f"Alert: {alert.alert_type} - {alert.message}")
        
    assert len(alerts) >= 2
    print("✅ Alerts Test Passed")

if __name__ == "__main__":
    try:
        test_nutrition_calculator()
        test_phase_tips()
        test_alerts()
        print("\n🎉 ALL TESTS PASSED")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
