import os
from coagent.agents import ChatAgent, ModelClient
from coagent.core import AgentSpec, new
from dotenv import load_dotenv

load_dotenv()

CONTENT = 'content'

with open("prompts/content_prompt.txt", "r", encoding="utf-8") as f:
    content_prompt = f.read()


content_agent = AgentSpec(
    CONTENT,
    new(
        ChatAgent,
        system=content_prompt,
        client=ModelClient(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
    ),
)
