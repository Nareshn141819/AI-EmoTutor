import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def tutor_mode(emotion):
    if emotion == "confusion":
        return "simple"
    elif emotion in ["anger", "sadness"]:
        return "encourage"
    elif emotion == "joy":
        return "challenge"
    return "normal"


def generate_response(question, mode):
    prompt = f"""
You are a friendly AI tutor.

Student said: "{question}"

Emotion: {mode}

Give a helpful, clear answer.
If emotion is sad → be supportive.
If excited → encourage.
If confused → explain step by step.
"""

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        text = response.output[0].content[0].text
        print("🤖 Response:", text)
        return text
    except Exception as e:
        print("❌ Error:", e)
        return "Error"
        
