"""
Chatbot API endpoints.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chatbot import get_ai_response, get_safety_response
from app.utils.safety import is_obviously_off_topic, validate_topic_with_ai
from app.utils.logging import log_request, log_response, log_error
import time

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the reproductive health education assistant.
    
    - **message**: Your question or message to the chatbot
    
    Returns educational information about reproductive health topics.
    """
    start_time = time.time()
    
    try:
        log_request("/chat", "POST", request.message)
        
        if not request.message or len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(request.message) > 1000:
            raise HTTPException(status_code=400, detail="Message too long (max 1000 characters)")
        
        # Check for safety triggers first
        safety_response = get_safety_response(request.message)
        
        if safety_response:
            duration = (time.time() - start_time) * 1000
            log_response("/chat", "safety_triggered", duration)
            return ChatResponse(
                response=safety_response,
                safety_triggered=True
            )
        
        # Validate topic relevance - Two-layer approach
        # Layer 1: Quick keyword-based check
        if is_obviously_off_topic(request.message):
            duration = (time.time() - start_time) * 1000
            log_response("/chat", "off_topic", duration)
            return ChatResponse(
                response="""I'm a specialized reproductive health education assistant. I can only answer questions related to:

• Menstrual cycles and periods
• Pregnancy and fertility
• Reproductive health and anatomy
• Hormones and women's health
• Gynecological conditions (PCOS, endometriosis, etc.)

Your question appears to be about a different topic. Please ask me about reproductive health, and I'll be happy to help! 😊""",
                safety_triggered=False
            )
        
        # Layer 2: AI-powered validation for ambiguous cases
        if not validate_topic_with_ai(request.message):
            duration = (time.time() - start_time) * 1000
            log_response("/chat", "off_topic_ai", duration)
            return ChatResponse(
                response="""I'm a specialized reproductive health education assistant. I can only answer questions related to:

• Menstrual cycles and periods
• Pregnancy and fertility
• Reproductive health and anatomy
• Hormones and women's health
• Gynecological conditions (PCOS, endometriosis, etc.)

Your question doesn't seem to be related to reproductive health. If you have questions about periods, pregnancy, fertility, or women's health, I'm here to help! 😊""",
                safety_triggered=False
            )
        
        # Get AI response for valid health-related questions
        ai_response = get_ai_response(request.message)
        
        duration = (time.time() - start_time) * 1000
        log_response("/chat", "success", duration)
        
        return ChatResponse(
            response=ai_response,
            safety_triggered=False
        )
    
    except HTTPException:
        raise
    except Exception as e:
        log_error("/chat", e)
        raise HTTPException(status_code=500, detail="Internal server error")
