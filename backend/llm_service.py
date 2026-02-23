from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-1.5-flash"


def generate_medical_response(query, context, structured_data=None, mode="qa"):

    # Reduce context size for performance
    context = context[:4000]

    if mode == "summary":

        prompt = f"""
You are a medical document analysis assistant.

Provide a structured summary of the report.
Use only the provided context.
Do not add any external information.

Context:
{context}
"""

    else:

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
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"