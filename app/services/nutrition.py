from typing import List, Dict
from app.models.schemas import (
    NutritionProfileRequest, NutritionPlanResponse, NutritionGoal, ActivityLevel,
    DailyNutritionTip, CyclePhase, NutrientInfo, NutritionAlert, SymptomData, LifestyleData
)

class NutritionService:
    @staticmethod
    def calculate_daily_needs(profile: NutritionProfileRequest) -> NutritionPlanResponse:
        """
        Calculate daily calorie and macro requirements based on user profile.
        Using Mifflin-St Jeor Equation for Women.
        """
        # 1. Calculate BMR (Basal Metabolic Rate)
        # BMR = 10W + 6.25H - 5A - 161
        bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * profile.age) - 161

        # 2. Calculate TDEE (Total Daily Energy Expenditure)
        activity_multipliers = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.ACTIVE: 1.725,
            ActivityLevel.VERY_ACTIVE: 1.9
        }
        tdee = bmr * activity_multipliers[profile.activity_level]

        # 3. Adjust for Goal
        goal_adjustment = 0
        if profile.goal == NutritionGoal.WEIGHT_LOSS:
            goal_adjustment = -500
        elif profile.goal == NutritionGoal.WEIGHT_GAIN:
            goal_adjustment = 500
        
        daily_calories = int(tdee + goal_adjustment)
        
        # Ensure calories don't drop too low
        if daily_calories < 1200:
            daily_calories = 1200

        # 4. Calculate Macros (Approximate split: 30% P, 35% C, 35% F)
        # Protein: 4 cal/g, Carbs: 4 cal/g, Fats: 9 cal/g
        protein_g = int((daily_calories * 0.30) / 4)
        carbs_g = int((daily_calories * 0.35) / 4)
        fats_g = int((daily_calories * 0.35) / 9)

        # 5. Water Intake (approx 35ml per kg)
        water_liters = round((profile.weight * 0.035), 1)

        # 6. BMI
        height_m = profile.height / 100
        bmi = round(profile.weight / (height_m * height_m), 1)
        
        bmi_category = "Normal"
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi >= 25 and bmi < 30:
            bmi_category = "Overweight"
        elif bmi >= 30:
            bmi_category = "Obese"

        return NutritionPlanResponse(
            calories=daily_calories,
            protein=protein_g,
            carbs=carbs_g,
            fats=fats_g,
            water_intake=water_liters,
            bmi=bmi,
            bmi_category=bmi_category
        )

    @staticmethod
    def get_phase_nutrition(cycle_day: int, cycle_length: int = 28) -> DailyNutritionTip:
        """
        Get nutrition tips based on the menstrual cycle phase.
        """
        # Determine Phase
        # Assuming standard 28 day cycle for simplicity if not provided, 
        # but logic scales roughly.
        
        # Normalize day if > cycle_length
        current_day = ((cycle_day - 1) % cycle_length) + 1
        
        # Approximate phases
        # Menstrual: 1-5
        # Follicular: 6-13
        # Ovulation: 14
        # Luteal: 15-28
        
        if 1 <= current_day <= 5:
            phase = CyclePhase.MENSTRUAL
            focus = "Iron Replenishment & Hydration"
            eat = ["Spinach", "Beetroot", "Jaggery", "Dates", "Red Meat/Eggs", "Warm Soups"]
            avoid = ["Caffeine (inhibits iron absorption)", "Salty foods (bloating)", "Cold foods"]
            tip = "Your iron levels drop during periods. Pair iron-rich foods with Vitamin C (like lemon/oranges) for better absorption."
            
        elif 6 <= current_day <= 13:
            phase = CyclePhase.FOLLICULAR
            focus = "Energy Boosting & Balanced Carbs"
            eat = ["Oats", "Quinoa", "Berries", "Nuts & Seeds", "Fermented foods (Yogurt)"]
            avoid = ["Heavy, greasy foods", "Excess sugar"]
            tip = "Estrogen is rising! You have more energy now. Focus on complex carbs and healthy fats to sustain this energy."
            
        elif current_day == 14 or (cycle_length/2 - 1 <= current_day <= cycle_length/2 + 1):
            phase = CyclePhase.OVULATION
            focus = "High Protein & Fiber"
            eat = ["Paneer/Tofu", "Chicken/Fish", "Lentils", "Leafy Greens", "Berries"]
            avoid = ["Processed carbs", "Excess salt"]
            tip = "Your body temperature rises slightly. Stay hydrated and eat fiber-rich foods to help eliminate excess estrogen."
            
        else:
            phase = CyclePhase.LUTEAL
            focus = "Bloating Control & Mood Support"
            eat = ["Bananas (Potassium)", "Dark Chocolate (Magnesium)", "Green Tea", "Sweet Potato", "Ginger"]
            avoid = ["Caffeine", "Alcohol", "Salty snacks", "Sugary treats"]
            tip = "PMS cravings might kick in. Choose dark chocolate over milk chocolate and drink herbal teas to reduce bloating."

        return DailyNutritionTip(
            phase=phase,
            focus=focus,
            foods_to_eat=eat,
            foods_to_avoid=avoid,
            tip_of_the_day=tip
        )

    @staticmethod
    def get_essential_nutrients() -> List[NutrientInfo]:
        """
        Return list of essential nutrients for women.
        """
        return [
            NutrientInfo(
                name="Iron",
                importance="Crucial for replacing blood loss during periods and preventing anemia/fatigue.",
                food_sources=["Spinach", "Beetroot", "Dates", "Jaggery", "Lentils", "Red meat"]
            ),
            NutrientInfo(
                name="Calcium",
                importance="Essential for bone health and reducing PMS symptoms like cramps.",
                food_sources=["Milk", "Curd/Yogurt", "Paneer", "Ragi", "Almonds", "Sesame seeds"]
            ),
            NutrientInfo(
                name="Vitamin D",
                importance="Regulates mood, supports bone health, and boosts immunity.",
                food_sources=["Sunlight (Morning)", "Mushrooms", "Fortified Milk", "Egg yolks", "Fatty fish"]
            ),
            NutrientInfo(
                name="Folic Acid (Vitamin B9)",
                importance="Vital for reproductive health and cell growth.",
                food_sources=["Dark leafy greens", "Citrus fruits", "Beans", "Peas", "Avocado"]
            ),
            NutrientInfo(
                name="Omega-3 Fatty Acids",
                importance="Reduces inflammation, balances hormones, and lowers stress.",
                food_sources=["Flax seeds", "Chia seeds", "Walnuts", "Fatty fish (Salmon/Mackerel)"]
            ),
            NutrientInfo(
                name="Magnesium",
                importance="Nature's relaxant - helps with sleep, cramps, and mood swings.",
                food_sources=["Dark Chocolate", "Pumpkin seeds", "Almonds", "Bananas", "Leafy greens"]
            )
        ]

    @staticmethod
    def generate_alerts(symptoms: SymptomData, lifestyle: LifestyleData) -> List[NutritionAlert]:
        """
        Generate nutrition-based alerts based on tracked symptoms.
        """
        alerts = []
        
        # 1. Iron Deficiency Alert
        if symptoms.energy_level and symptoms.energy_level <= 2:
            alerts.append(NutritionAlert(
                alert_type="Low Energy / Potential Iron Deficiency",
                severity="Medium",
                message="You've reported low energy levels recently.",
                recommendation="Boost your Iron intake with dates, spinach, or beetroot juice. Ensure you're sleeping enough."
            ))
            
        # 2. PMS/Bloating Alert
        if symptoms.bloating and symptoms.bloating >= 3:
            alerts.append(NutritionAlert(
                alert_type="Bloating Relief",
                severity="Medium",
                message="High bloating reported.",
                recommendation="Avoid salt and caffeine. Try drinking ginger tea, peppermint tea, or eating a banana for potassium."
            ))
            
        # 3. Mood/Stress Alert
        if (symptoms.mood_changes and symptoms.mood_changes >= 3) or (lifestyle.stress_level and lifestyle.stress_level >= 4):
            alerts.append(NutritionAlert(
                alert_type="Mood & Stress Support",
                severity="High",
                message="High stress or mood swings detected.",
                recommendation="Focus on Omega-3s (Walnuts/Chia seeds) and Magnesium (Dark Chocolate). Avoid sugar spikes."
            ))
            
        # 4. Cramps
        if symptoms.cramps and symptoms.cramps >= 3:
            alerts.append(NutritionAlert(
                alert_type="Cramp Relief",
                severity="High",
                message="Significant cramps reported.",
                recommendation="Increase Magnesium intake. Warm chamomile tea and calcium-rich foods can also help relax muscles."
            ))

        return alerts
