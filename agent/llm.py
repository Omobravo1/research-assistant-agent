import os

from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_llm(user_prompt: str) -> str:
    """
    Send a prompt to OpenAI and return the response.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    return response.output_text