# 🚀 CodeBloom - Reproductive Health API

A professional, modular API that combines **AI-powered Chatbot** and **Advanced Menstrual Cycle Prediction** functionalities into a single service.

## ✨ Features

- **🤖 Reproductive Health Chatbot**: AI-powered educational assistant using Groq (Llama 3)
- **📊 Cycle Predictor**: LSTM/GRU-based cycle prediction for basic tracking
- **🔮 Enhanced Predictor**: Multi-feature prediction using symptoms, lifestyle, and flow data
- **❤️ Unified Health Checks**: Monitor all services from a single endpoint
- **🛡️ Safety First**: Built-in safety checks for medical content

---

## 🛠️ Prerequisites & Installation

### 1. Requirements
- Python 3.10+
- Groq API Key (for chatbot)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: If you don't have a `requirements.txt`, install manually:*
```bash
pip install fastapi uvicorn groq pydantic numpy torch python-dotenv
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
PORT=8000
```

---

## 🚀 Running the API

### Method 1: Using Python Module (Recommended)
```bash
python -m app.main
```

### Method 2: Using Uvicorn Directly
```bash
uvicorn app.main:app --reload
```

The server will start on **http://localhost:8000**

---

## 📚 API Documentation

### 1. 💬 Chatbot
**Endpoint:** `POST /chat`

Ask educational questions about reproductive health.

**Request:**
```json
{
  "message": "What is ovulation?"
}
```

**Response:**
```json
{
  "response": "Ovulation is the phase...",
  "safety_triggered": false
}
```

### 2. 📊 Simple Cycle Prediction
**Endpoint:** `POST /predict`

Basic prediction using only past cycle lengths.

**Request:**
```json
{
  "past_cycles": [28, 30, 27, 29, 28],
  "last_period_date": "2025-01-15",
  "framework": "pytorch"
}
```

### 3. 🔮 Enhanced Cycle Prediction (New!)
**Endpoint:** `POST /predict/enhanced`

Advanced prediction using symptoms, flow intensity, and lifestyle factors for higher accuracy (92-95%).

**Request:**
```json
{
  "cycle_records": [
    {
      "cycle_length": 28,
      "date": "2024-11-15",
      "symptoms": {
        "cramps": 3,           
        "mood_changes": 2,     
        "energy_level": 4      
      },
      "flow_intensity": "medium", 
      "lifestyle": {
        "stress_level": 2,  
        "sleep_quality": 5    
      }
    }
  ],
  "last_period_date": "2025-03-09",
  "framework": "pytorch"
}
```

**Response Includes:**
- Predicted cycle length & next period date
- **Confidence Score** (0-100%)
- **Health Insights** (Personalized tips)
- **Feature Importance** (What affects your cycle most)

### 4. ❤️ Health Check
**Endpoint:** `GET /health`

Check the status of the API and ML models.

---

## 📂 Project Structure

```
CodeBloom/
├── app/
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration
│   ├── models/           # Pydantic schemas
│   ├── services/         # Business logic (chatbot, predictor)
│   ├── routers/          # API endpoints
│   ├── ml/               # Machine learning models & feature engineering
│   └── utils/            # Utilities (logging, safety, confidence)
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```

---

## ❓ Troubleshooting

- **Port Already in Use?** Change the port in `.env` or use `$env:PORT=5000 python -m app.main`
- **Missing Groq Key?** Ensure `GROQ_API_KEY` is set in `.env`
- **PyTorch Error?** Install CPU version: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

---

## 🔗 Interactive Docs
Visit **http://localhost:8000/docs** to test all endpoints interactively in your browser.
