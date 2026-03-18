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
You are an AI EmoTutor inside an educational app.

Your job:
- Help students understand concepts clearly
- Adapt your teaching style based on emotion

Student Question:
{question}

Detected Teaching Mode:
{mode}

Instructions:
- If mode is "simple": explain in very easy terms
- If mode is "encourage": be supportive and motivating
- If mode is "challenge": ask a follow-up question or deepen thinking
- If mode is "normal": give a balanced explanation

Keep answer:
- Clear
- Short (3–5 lines)
- Friendly tone
- No extra unnecessary info

Now respond as the tutor:
"""

    try:
        response = model.generate_content(prompt)
        print("Gemini success")
        return response.text.strip()
    except Exception as e:
        print("Gemini AI ERROR:", e)
        return "Error generating response"
