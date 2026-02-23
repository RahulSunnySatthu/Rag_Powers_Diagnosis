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

    # ⚡ Reduce prompt size impact
    context = context[:4000]  # prevent very large context slowing response

    if mode == "summary":

        prompt = f"""
You are a medical document analysis assistant.

Provide a structured summary of the report.
Use only the provided context.
Do not add external information.

Context:
{context}
"""

    else:
        prompt = f"""
You are a medical document analysis assistant.

STRICT INSTRUCTIONS:
- Answer ONLY the user's question.
- Do NOT summarize entire report.
- Base answer ONLY on provided context.
- If answer is not present, say:
  "The uploaded document does not contain enough information."

User Question:
{query}

Relevant Context:
{context}

Provide a concise answer.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"