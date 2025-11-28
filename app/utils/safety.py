"""
Safety check utilities for chatbot input validation.
"""

from app.models.constants import (
    EMERGENCY_KEYWORDS,
    UNSAFE_KEYWORDS,
    HEALTH_RELATED_KEYWORDS,
    OFF_TOPIC_KEYWORDS,
    TOPIC_VALIDATION_PROMPT,
)
from app.config import client, MODEL_NAME


def check_emergency(message: str) -> bool:
    """Check if message contains emergency keywords."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)


def check_unsafe(message: str) -> bool:
    """Check if message contains unsafe content keywords."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in UNSAFE_KEYWORDS)


def is_obviously_off_topic(message: str) -> bool:
    """
    Quick check for obviously off-topic questions using keywords.
    
    Returns True if the message is clearly off-topic.
    """
    message_lower = message.lower()
    
    # Check for off-topic keywords
    has_off_topic = any(keyword in message_lower for keyword in OFF_TOPIC_KEYWORDS)
    
    # Check for health-related keywords
    has_health_keywords = any(keyword in message_lower for keyword in HEALTH_RELATED_KEYWORDS)
    
    # If it has off-topic keywords and no health keywords, it's likely off-topic
    if has_off_topic and not has_health_keywords:
        return True
    
    return False


def validate_topic_with_ai(message: str) -> bool:
    """
    Use AI to validate if the question is related to reproductive health.
    
    Returns True if the topic is relevant to reproductive health.
    """
    if not client:
        # If Groq client is not available, be permissive
        return True
    
    try:
        validation_response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": TOPIC_VALIDATION_PROMPT.format(message=message)}
            ],
            model=MODEL_NAME,
            temperature=0.3,  # Lower temperature for more consistent classification
            max_tokens=10
        )
        
        classification = validation_response.choices[0].message.content.strip().upper()
        return "RELEVANT" in classification
        
    except Exception:
        # If AI validation fails, be permissive and allow the question
        return True
