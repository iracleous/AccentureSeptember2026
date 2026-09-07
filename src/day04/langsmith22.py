"""
langsmith
"""

from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()


@traceable
def classify_question(question: str) -> str:
    """Classify the question type."""
    return "billing" if "refund" in question.lower() else "general"


@traceable
def generate_answer(question: str, category: str) -> str:
    """Generate an answer based on category."""
    if category == "billing":
        return "Refunds are issued within 30 days."
    return "Please contact support."


question = "What's your refund policy?"
category = classify_question(question)
answer = generate_answer(question, category)

print(f"Q: {question}")
print(f"Category: {category}")
print(f"A: {answer}")
print("\nOpen smith.langchain.com to see the traces.")
