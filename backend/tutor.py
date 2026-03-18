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

    # 🛑 handle empty / bad input
    if not question or question.strip() == "":
        return "Please ask a valid question."

    system_prompt = f"""
You are an AI EmoTutor.

IMPORTANT:
- Answer ONLY the student's question
- Do NOT explain the input or mode
- Do NOT mention "Student voice input" or "Mode"
- Do NOT describe voice, tone, or speaking style

Teaching Mode: {mode}

Rules:
- Start answer with: Here is your answer:
- Keep answer short (3–5 lines)
- Use simple student-friendly language

Student Question:
{question}
"""

    try:
        response = model.generate_content({question})

        if not response.text:
            return "No response generated"

        return response.text.strip()

    except Exception as e:
        print("Gemini ERROR:", e)
        return "Error generating response"
