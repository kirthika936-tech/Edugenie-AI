"""
EduGenie - Question Answering Module

This module handles the Question & Answer feature of EduGenie.

Flow:

Student Question
       ↓
     qna.py
       ↓
 Gemini Client
       ↓
 Generated Answer
       ↓
    FastAPI
       ↓
   Frontend
"""

from gemini_client import generate_text
def answer_question(question):
    # your logic here
    return "Answer"

async def answer_question(question: str) -> str:
    """
    Generate an educational answer for the
    question provided by the student.

    Args:
        question (str):
            The question entered by the student.

    Returns:
        str:
            AI-generated answer from Gemini.
    """

    prompt = f"""
You are EduGenie, an AI-powered learning assistant.

Answer the student's question clearly and accurately.

Student's Question:
{question}

Instructions:

1. Give a direct answer to the question.
2. Explain the answer in simple and easy-to-understand language.
3. If necessary, provide a small example.
4. Use bullet points when they make the explanation clearer.
5. Keep the answer suitable for a student.
6. Do not make up facts.
7. If the question is unclear, explain what information is needed.
"""

    answer = generate_text(
        prompt,
        system_instruction="""
You are EduGenie, a helpful educational AI assistant.

Your purpose is to help students understand
academic and general knowledge topics.

Always:
- Be clear
- Be accurate
- Be concise
- Explain difficult concepts simply
- Use examples when useful
- Avoid unnecessary complicated terminology
""",
        temperature=0.3,
        max_output_tokens=1000,
    )

    return answer