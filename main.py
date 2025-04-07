import asyncio
import os
from dotenv import load_dotenv
from coagent.runtimes import LocalRuntime
from coagent.agents import ChatMessage

from agents.grammar_agent import grammar_agent
from agents.content_agent import content_agent
from agents.match_agent import match_agent
from agents.score_agent import score_agent
from utils.pdf_reader import read_pdf_text

load_dotenv()
AGENTS = [grammar_agent, content_agent, match_agent, score_agent]

def read_txt(path: str) -> str:
    """Read plain text from a .txt file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

async def main():
    # === Step 1: Get resume and JD file paths ===
    resume_path = input("Enter the path to your resume (PDF file):\n")
    jd_path = input("Enter the path to the job description (TXT or PDF file):\n")

    # === Step 2: Extract text ===
    resume_text = read_pdf_text(resume_path)

    if jd_path.lower().endswith(".pdf"):
        jd_text = read_pdf_text(jd_path)
    else:
        jd_text = read_txt(jd_path)

    # === Step 3: Register agents and run them sequentially ===
    async with LocalRuntime() as runtime:
        for agent in AGENTS:
            await runtime.register(agent)

        # === Step 3.5: Score ===
        print("\n✅ Score Result:\n")
        score_result = await score_agent.run(
            ChatMessage(role="user", content=resume_text).encode(),
            stream=True,
        )
        async for chunk in score_result:
            msg = ChatMessage.decode(chunk)
            print(msg.content, end="", flush=True)

        # === Step 4: Grammar Optimization ===
        print("\n✅ Grammar Optimization Result:\n")
        grammar_result = await grammar_agent.run(
            ChatMessage(role="user", content=resume_text).encode(),
            stream=True,
        )
        grammar_text = ""
        async for chunk in grammar_result:
            msg = ChatMessage.decode(chunk)
            print(msg.content, end="", flush=True)
            grammar_text += msg.content

        # === Step 5: Content Optimization ===
        print("\n\n✅ Content Optimization Result:\n")
        content_result = await content_agent.run(
            ChatMessage(role="user", content=grammar_text).encode(),
            stream=True,
        )
        content_text = ""
        async for chunk in content_result:
            msg = ChatMessage.decode(chunk)
            print(msg.content, end="", flush=True)
            content_text += msg.content

        # === Step 6: Resume-JD Matching Analysis ===
        print("\n\n✅ Resume-to-JD Matching Report:\n")
        combined_input = f"[Resume]:\n{content_text}\n\n[Job Description]:\n{jd_text}"
        match_result = await match_agent.run(
            ChatMessage(role="user", content=combined_input).encode(),
            stream=True,
        )
        match_text = ""
        async for chunk in match_result:
            msg = ChatMessage.decode(chunk)
            print(msg.content, end="", flush=True)
            match_text += msg.content

if __name__ == "__main__":
    asyncio.run(main())