from coagent.core import BaseAgent
from coagent.agents import ChatMessage

class OptimizePipelineAgent(BaseAgent):
    def __init__(self, grammar, content, match, jd_text):
        super().__init__()
        self.grammar = grammar
        self.content = content
        self.match = match
        self.jd_text = jd_text

    async def run(self, input_bytes: bytes, stream: bool = False):
        # Step 1: Grammar
        grammar_result = await self.grammar.run(input_bytes)
        async for chunk in grammar_result:
            grammar_text = ChatMessage.decode(chunk).content
            break

        # Step 2: Content
        content_result = await self.content.run(
            ChatMessage(role="user", content=grammar_text).encode()
        )
        async for chunk in content_result:
            content_text = ChatMessage.decode(chunk).content
            break

        # Step 3: Match
        match_input = ChatMessage(
            role="user",
            content=f"[Resume]:\n{content_text}\n\n[Job Description]:\n{self.jd_text}",
        )
        match_result = await self.match.run(match_input.encode())
        async for chunk in match_result:
            return chunk
