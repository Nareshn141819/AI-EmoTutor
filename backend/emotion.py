# emotion.py

def detect_emotion(text):

    text = text.lower()

    if any(word in text for word in ["confused", "don't understand", "doubt"]):
        return "confusion"

    elif any(word in text for word in ["angry", "frustrated", "hate"]):
        return "anger"

    elif any(word in text for word in ["sad", "tired", "upset"]):
        return "sadness"

    elif any(word in text for word in ["happy", "good", "great"]):
        return "joy"

    return "neutral"
