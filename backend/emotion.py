# emotion.py
def detect_emotion(text):

    text = text.lower()

    if any(word in text for word in ["confused", "don't understand", "what", "why"]):
        return "confusion"

    elif any(word in text for word in ["sad", "tired", "hard", "difficult"]):
        return "sadness"

    elif any(word in text for word in ["angry", "frustrated", "annoyed"]):
        return "anger"

    elif any(word in text for word in ["easy", "great", "understood", "good"]):
        return "joy"

    return "neutral"
