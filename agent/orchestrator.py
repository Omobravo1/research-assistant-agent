"""
Agent Orchestrator

This file is responsible for deciding which tool
should answer the user's request.
"""

from agent.llm import ask_llm


class ResearchAgent:
    """
    Main AI agent.

    For now, every request goes directly to the LLM.

    Later this class will decide whether to:

    - Search uploaded PDFs
    - Search the web
    - Use memory
    - Generate reports
    """

    def process(self, user_input: str) -> str:

        return ask_llm(user_input)