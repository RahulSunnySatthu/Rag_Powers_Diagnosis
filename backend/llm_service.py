import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_medical_response(query, context, structured_data=None, mode="qa"):

    if mode == "summary":

        prompt = f"""
You are a medical document analysis assistant.

Provide a structured summary of the report.

Use only the provided context.
Do not add any external information.

Context:
{context}
"""

    else:  # STRICT QUESTION ANSWERING MODE

        prompt = f"""
You are a medical document analysis assistant.

STRICT INSTRUCTIONS:

- Answer ONLY the user's question.
- Do NOT summarize the entire report.
- Do NOT include unrelated test values.
- Do NOT repeat full document details.
- Base answer ONLY on provided context.
- If the answer is not clearly present, say:
  "The uploaded document does not contain enough information to answer this question."
- Keep the answer concise and focused.

User Question:
{query}

Relevant Context:
{context}

Provide a direct, question-specific answer.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
