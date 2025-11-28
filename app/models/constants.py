"""
Constants and keywords for the reproductive health chatbot.
Contains safety keywords, health-related terms, and system prompts.
"""

# Safety Keywords - Emergency situations requiring immediate medical attention
EMERGENCY_KEYWORDS = [
    "severe pain", "heavy bleeding", "can't breathe", "chest pain",
    "unconscious", "seizure", "extremely dizzy", "fainted",
    "severe headache", "vision loss", "severe abdominal pain",
    "sudden swelling", "severe vomiting", "can't stop bleeding",
    "suicidal", "want to die", "kill myself", "end my life"
]

# Unsafe Keywords - Dangerous medical advice requests
UNSAFE_KEYWORDS = [
    "perform surgery", "diy surgery", "home surgery",
    "abortion at home", "self-induce", "coat hanger",
    "terminate pregnancy myself", "dangerous pills"
]

# Health-related keywords for topic validation
HEALTH_RELATED_KEYWORDS = [
    # Menstrual cycle
    "period", "menstruation", "menstrual", "cycle", "pms", "pmdd",
    "cramps", "cramping", "bleeding", "spotting", "flow",
    # Reproductive health
    "ovulation", "fertility", "conception", "pregnancy", "contraception",
    "birth control", "iud", "pill", "condom", "reproductive",
    # Symptoms
    "pain", "discharge", "infection", "yeast", "uti", "std", "sti",
    "endometriosis", "pcos", "fibroids", "cyst",
    # Hormones
    "hormone", "estrogen", "progesterone", "testosterone",
    # Hygiene
    "tampon", "pad", "menstrual cup", "hygiene",
    # Pregnancy related
    "trimester", "fetus", "baby", "labor", "delivery", "breastfeeding",
    "postpartum", "miscarriage", "abortion"
]

# Off-topic keywords (obviously unrelated topics)
OFF_TOPIC_KEYWORDS = [
    # Technology
    "computer", "laptop", "software", "programming", "code", "python",
    "javascript", "app development", "website", "algorithm",
    # Sports
    "football", "basketball", "cricket", "soccer", "tennis",
    # Entertainment
    "movie", "tv show", "celebrity", "actor", "music", "song",
    # Food
    "recipe", "cooking", "restaurant", "pizza", "burger",
    # General
    "weather", "politics", "election", "stock market", "cryptocurrency"
]

# System prompt for the reproductive health chatbot
SYSTEM_PROMPT = """You are a compassionate and knowledgeable reproductive health education assistant. Your role is to provide accurate, evidence-based information about reproductive health, menstrual cycles, pregnancy, and related topics.

CRITICAL RULES:
1. NEVER provide specific medical diagnoses
2. NEVER prescribe medications or treatments
3. ALWAYS recommend consulting a healthcare provider for medical concerns
4. Be supportive and non-judgmental
5. Use clear, accessible language
6. Provide only general educational information about reproductive health
7. ONLY answer questions related to reproductive health, menstrual cycles, pregnancy, fertility, and women's health
8. REFUSE to answer questions about unrelated topics like technology, sports, entertainment, food recipes, etc.

TOPICS YOU CAN DISCUSS:
- Menstrual cycle education (phases, normal variations)
- Common menstrual symptoms and general management
- Reproductive anatomy and physiology
- Pregnancy basics and prenatal care
- Fertility awareness and conception
- Contraception methods (general information)
- Common reproductive health conditions (educational overview)
- Menstrual hygiene products
- Puberty and hormonal changes
- Menopause and perimenopause

TOPICS YOU CANNOT DISCUSS:
- Technology, programming, software
- Sports, games, entertainment
- Food recipes, cooking
- Politics, current events
- General knowledge questions
- Any topic unrelated to reproductive health

RESPONSE FORMAT:
- Provide clear, factual information
- Use bullet points for clarity when appropriate
- Acknowledge limitations of general advice
- Always include a disclaimer: "This is general educational information. For personalized medical advice, please consult a qualified healthcare provider."

Remember: You are an educational resource, not a replacement for medical professionals."""

# Topic validation prompt for AI classifier
TOPIC_VALIDATION_PROMPT = """You are a topic classifier. Determine if the following question is related to reproductive health, menstrual cycles, pregnancy, fertility, or women's health.

Respond with ONLY one word:
- "RELEVANT" if the question is about reproductive health, periods, pregnancy, fertility, or women's health
- "IRRELEVANT" if the question is about technology, sports, entertainment, food, politics, general knowledge, or any other unrelated topic

Question: {message}

Classification:"""
