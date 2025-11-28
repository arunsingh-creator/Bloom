# Nutrition Section Implementation Walkthrough

I have successfully implemented the **Women Health App – Nutrition Section** with AI-based features.

## Features Implemented

### 1. AI Nutrition Calculator
-   **Functionality**: Calculates daily calorie, protein, carb, fat, and water requirements based on age, height, weight, activity level, and goal.
-   **Logic**: Uses the Mifflin-St Jeor equation tailored for women, with adjustments for weight loss/gain goals.
-   **API Endpoint**: `POST /nutrition/calculate`

### 2. Menstrual Phase-based Nutrition Tips
-   **Functionality**: Provides specific food recommendations and tips based on the current cycle day.
-   **Phases Covered**:
    -   **Menstrual**: Focus on Iron & Hydration.
    -   **Follicular**: Focus on Energy & Balanced Carbs.
    -   **Ovulation**: Focus on High Protein.
    -   **Luteal**: Focus on Bloating Control & Mood Support.
-   **API Endpoint**: `GET /nutrition/tips/{cycle_day}`

### 3. Essential Nutrients for Women
-   **Functionality**: Returns a list of key nutrients (Iron, Calcium, Vitamin D, Folic Acid, Omega-3) with their importance and food sources.
-   **API Endpoint**: `GET /nutrition/essentials`

### 4. Smart Nutrition Alerts
-   **Functionality**: Generates personalized alerts based on tracked symptoms (e.g., low energy -> Iron deficiency alert, high stress -> Magnesium recommendation).
-   **API Endpoint**: `POST /nutrition/alerts`

## Files Modified/Created

-   `app/models/schemas.py`: Added Pydantic models for nutrition profiles, plans, and tips.
-   `app/services/nutrition.py`: Implemented the core logic for calculations and recommendations.
-   `app/routers/nutrition.py`: Created the API endpoints.
-   `app/routers/__init__.py`: Exported the new router.
-   `app/main.py`: Registered the nutrition router.

## Verification

I created a verification script `verify_nutrition.py` to test the logic.
**Results**:
-   ✅ Calculator correctly adjusts calories for goals.
-   ✅ Phase tips return correct focus for each cycle phase.
-   ✅ Alerts are triggered correctly based on symptom thresholds.

## How to Use

1.  **Start the Server**:
    ```bash
    python app/main.py
    ```
2.  **Access Documentation**:
    Go to `http://localhost:8000/docs` to see the new Nutrition endpoints.
