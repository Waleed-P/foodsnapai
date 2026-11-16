import json
import logging
from typing import Any, Dict, List, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None  # type: ignore

from app.client import get_groq_client
from app.core.config import settings
from app.prompts import SYSTEM_PROMPT
from app.schemas import TOOLS
from app.tools import TOOL_FUNCTIONS

logger = logging.getLogger("agent.executor")


class Agent:
    def __init__(
        self,
        client: Optional[Any] = None,
        system: str = SYSTEM_PROMPT,
        tools: Optional[List[Dict[str, Any]]] = None,
        user_id: int = 1,
        auth_token: Optional[str] = None,
    ):
        self.client = client or get_groq_client()
        self.system = system
        self.tools = tools if tools is not None else TOOLS
        self.user_id = user_id
        self.auth_token = auth_token
        self.messages: List[Dict[str, Any]] = []

        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, message: str = "") -> str:
        if message:
            self.messages.append({"role": "user", "content": message})
        return self.execute()

    def execute(self, max_turns: int = 5) -> str:
        if self.client is None:
            return "The AI agent service is currently not connected to Groq. Please configure GROQ_API_KEY."

        turn = 0
        while turn < max_turns:
            turn += 1
            try:
                completion = self.client.chat.completions.create(
                    model=settings.groq_model,
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto",
                )
            except Exception as e:
                logger.error(f"Error querying Groq LLM: {e}")
                return f"I encountered an error analyzing your request: {str(e)}"

            response_message = completion.choices[0].message

            # Handle Tool Calls
            if response_message.tool_calls:
                self.messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except Exception:
                        function_args = {}

                    function_to_call = TOOL_FUNCTIONS.get(function_name)

                    if function_to_call is None:
                        tool_output = {"error": f"Unknown tool: {function_name}"}
                    else:
                        try:
                            # Inject context
                            tool_output = function_to_call(
                                user_id=self.user_id,
                                auth_token=self.auth_token,
                                **function_args,
                            )
                        except TypeError:
                            # In case tool only takes subset of args
                            try:
                                tool_output = function_to_call(
                                    user_id=self.user_id,
                                    **function_args,
                                )
                            except Exception as e:
                                tool_output = {"error": str(e)}
                        except Exception as e:
                            tool_output = {"error": str(e)}

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(tool_output, default=str),
                        }
                    )
                continue

            if response_message.content:
                self.messages.append(
                    {"role": "assistant", "content": response_message.content}
                )
                return response_message.content

        return "I completed looking up your nutrition history, but could not finalize a summary."
