"""
Chatbot service for reproductive health education.
"""

from typing import Optional
from fastapi import HTTPException

from app.config import client, MODEL_NAME
from app.models.constants import SYSTEM_PROMPT
from app.utils.safety import check_emergency, check_unsafe


def get_safety_response(message: str) -> Optional[str]:
    """
    Check for safety triggers and return appropriate response.
    
    Args:
        message: User's message
        
    Returns:
        Safety response if triggered, None otherwise
    """
    if check_emergency(message):
        return """🚨 **URGENT: Your message indicates a potentially serious medical situation.**

Please seek immediate medical attention:
- Call emergency services (911 in US, 112 in EU, or your local emergency number)
- Go to the nearest emergency room
- Contact your doctor immediately

Your health and safety are the top priority. Medical professionals can provide the urgent care you need."""

    if check_unsafe(message):
        return """I cannot provide information on this topic as it could be harmful to your health and safety.

If you're experiencing a crisis or having thoughts of self-harm:
- **Crisis Hotline:** 988 (Suicide & Crisis Lifeline - US)
- **International:** https://findahelpline.com

For reproductive health concerns, please speak with:
- A licensed healthcare provider
- Planned Parenthood or similar clinics
- A trusted counselor or therapist

Your wellbeing matters, and there are professionals ready to help you safely."""

    return None


def get_ai_response(message: str) -> str:
    """
    Get AI-generated response for reproductive health questions.
    
    Args:
        message: User's question
        
    Returns:
        AI-generated educational response
        
    Raises:
        HTTPException: If AI service fails
    """
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Chatbot service is not configured. Please set GROQ_API_KEY environment variable."
        )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        # Additional safety check
        if any(word in ai_response.lower() for word in ["i diagnose", "you have", "you need to take"]):
            ai_response += "\n\n⚠️ Remember: This is educational information only, not a diagnosis or prescription. Always consult a healthcare provider for personalized medical advice."
        
        return ai_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
