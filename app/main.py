"""
Main FastAPI application entry point.
"""

import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import chatbot_router, prediction_router, pcos_router, thyroid_router
from app.config import GROQ_API_KEY, MODEL_NAME
from app.ml.model_factory import get_framework_availability
from app.utils.logging import logger, log_info

# Initialize FastAPI app
app = FastAPI(
    title="Reproductive Health Combined API",
    description="AI-powered chatbot and menstrual cycle prediction in one API",
    version="2.0.0"
)

# Configure allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React/Next.js dev
    "http://localhost:5173",      # Vite dev
    "http://localhost:8000",      # API docs
    "http://127.0.0.1:8000",      # API docs alternative
    # Add your production domains here
    # "https://yourdomain.com",
]

# Enable CORS with security restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # Set to True only if using authentication
    allow_methods=["GET", "POST"],  # Only allow needed methods
    allow_headers=["Content-Type", "Accept"],
)

# Include routers
app.include_router(chatbot_router)
app.include_router(prediction_router)
app.include_router(pcos_router)
app.include_router(thyroid_router)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    log_info("Root endpoint accessed")
    return {
        "status": "online",
        "service": "Combined Reproductive Health API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "chatbot": "Available at /chat",
            "cycle_prediction": "Available at /predict",
            "pcos_risk": "Available at /pcos/risk-assessment",
            "thyroid_tracker": "Available at /thyroid"
        },
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    frameworks = get_framework_availability()
    available_frameworks = [k for k, v in frameworks.items() if v]
    
    groq_configured = bool(GROQ_API_KEY)
    
    log_info(f"Health check - Groq: {groq_configured}, Frameworks: {available_frameworks}")
    
    return {
        "status": "healthy",
        "chatbot": {
            "status": "operational" if groq_configured else "not configured",
            "groq_configured": groq_configured,
            "model": MODEL_NAME
        },
        "cycle_predictor": {
            "status": "operational" if available_frameworks else "no ML frameworks available",
            "available_frameworks": available_frameworks
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/favicon.ico")
async def favicon():
    """Favicon handler to prevent 404 errors."""
    return JSONResponse(content={"message": "No favicon"})


if __name__ == "__main__":
    import uvicorn
    
    # Import to ensure framework availability is set
    from app.ml import model_factory
    
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    frameworks = get_framework_availability()
    
    print("=" * 70)
    print("🚀 REPRODUCTIVE HEALTH API")
    print("=" * 70)
    print(f"📍 Server: http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print("=" * 70)
    print("CHATBOT STATUS:")
    print(f"  🤖 Model: {MODEL_NAME}")
    print(f"  🔑 Groq API Key: {'✅ Set' if GROQ_API_KEY else '❌ Missing'}")
    print("=" * 70)
    print("CYCLE PREDICTOR STATUS:")
    print(f"  🔬 PyTorch: {'✅ Available' if frameworks.get('pytorch', False) else '❌ Not installed'}")
    print("=" * 70)
    print("ENDPOINTS:")
    print("  💬 Chatbot: POST /chat")
    print("  📊 Cycle Prediction: POST /predict")
    print("  ⚠️  PCOS Risk: POST /pcos/risk-assessment")
    print("  🦋 Thyroid Tracker: POST /thyroid/risk-assessment")
    print("  ❤️  Health Check: GET /health")
    print("=" * 70)
    
    log_info("Starting CodeBloom API server")
    uvicorn.run(app, host="0.0.0.0", port=port)
