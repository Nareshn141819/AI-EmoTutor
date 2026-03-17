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
    You are an AI tutor.

    Student question: {question}

    Teaching style: {mode}

    Give a clear answer.
    """
    
    try:
        response = model.generate_content(f"Question: {question}, Mode: {mode}")
        print("success")
        return response.text
    except Exception as e:
        print("Gemini AI ERROR:", e)
        return "Error generating response"
