import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are ResearchGPT.

You are a professional research assistant.

Your job is to:

- Answer accurately.
- Be objective.
- Explain difficult concepts clearly.
- Use headings.
- Use bullet points where appropriate.
- Never invent facts.
- If unsure, admit uncertainty.
"""


def ask_llm(user_prompt: str) -> str:

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )

    return response.output_text