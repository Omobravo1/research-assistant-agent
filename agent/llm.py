import os

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Please check your .env file."
    )

# Create a reusable client
client = OpenAI(api_key=api_key)


def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to OpenAI and returns the model's response.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text