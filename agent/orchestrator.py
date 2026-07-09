from agent.llm import ask_llm


class ResearchAgent:

    def process(
        self,
        user_input,
        context=None,
    ):

        if context:

            prompt = f"""
Use ONLY the information below to answer the user's question.

Context

{context}

Question

{user_input}
"""

            return ask_llm(prompt)

        return ask_llm(user_input)