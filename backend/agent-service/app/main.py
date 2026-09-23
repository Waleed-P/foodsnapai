from app.ai_agent.agent import Agent
from app.ai_agent.client import client
from app.ai_agent.schemas import TOOLS
from app.ai_agent.prompts import SYSTEM_PROMPT


agent = Agent(
    client=client,
    system=SYSTEM_PROMPT,
    tools=TOOLS,
)


response = agent(
    "provide my nutrition intake on yesterday"
)



print("\nFinal answer:")
print(response)