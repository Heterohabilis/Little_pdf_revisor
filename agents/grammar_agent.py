import os
from coagent.agents import ChatAgent, ModelClient
from coagent.core import AgentSpec, new
from dotenv import load_dotenv

load_dotenv()

GRAMMAR = 'grammar'

with open("prompts/grammar_prompt.txt", "r", encoding="utf-8") as f:
    grammar_prompt = f.read()

grammar_agent = AgentSpec(
    GRAMMAR,
    new(
        ChatAgent,
        system= grammar_prompt,
        client=ModelClient(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
    ),
)
