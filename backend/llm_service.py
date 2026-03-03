from google import genai
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _strip_markdown(text: str) -> str:
    """Remove markdown syntax for clean plain-text display."""
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)  # headings
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.+?)\*", r"\1", text)  # italic
    text = re.sub(r"__(.+?)__", r"\1", text)  # bold alt
    text = re.sub(r"_(.+?)_", r"\1", text)  # italic alt
    text = re.sub(r"^[-*]\s+", "• ", text, flags=re.MULTILINE)  # normalize bullets
    text = re.sub(r"^\d+\.\s+", "• ", text, flags=re.MULTILINE)  # numbered to bullet
    text = re.sub(r"\n{3,}", "\n\n", text)  # collapse extra newlines
    return text.strip()

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

Provide a short, structured summary of the report.

RULES:
- Use ONLY plain text. NO markdown (no #, **, *, ##, -, numbered lists, etc.).
- Start with a 1-2 sentence overview.
- Use bullet points with • for key findings, values, or sections.
- Keep each bullet brief (one line).
- Base everything ONLY on the provided context. Do not add external information.
- At the END, add a "Document Impression" section: exactly 4 lines summarizing the overall clinical impression, key takeaways, or conclusion of the document. Each line should be one sentence.

Context:
{context}

Output format:
1. Short overview sentence.
2. Bullet points with • for main points.
3. Document Impression: (4 lines, each a concise impression/conclusion)
"""

    else:

        prompt = f"""
You are a medical document analysis assistant.

STRICT INSTRUCTIONS:
- Answer ONLY the user's question.
- Use ONLY plain text. NO markdown (no #, **, *, ##, etc.).
- For lists or multiple points, use bullet points with •.
- Keep answers short: brief description + bullets where helpful.
- Base answer ONLY on provided context.
- If the answer is not clearly present, say:
  "The uploaded document does not contain enough information to answer this question."

User Question:
{query}

Relevant Context:
{context}

Provide a direct, polished answer in plain text.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw = response.text.strip()
        return _strip_markdown(raw)

    except Exception as e:
        return f"Error generating response: {str(e)}"