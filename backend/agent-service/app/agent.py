import json

from groq import Groq

from app.ai_agent.tools.daily_nutrition import get_daily_nutrition
from app.ai_agent.tools.food_history import get_food_history
from app.ai_agent.tools.nutrition_history import get_nutrition_history
from app.ai_agent.schemas import TOOLS


TOOL_FUNCTIONS = {
    "get_food_history": get_food_history,
    "get_daily_nutrition": get_daily_nutrition,
    "get_nutrition_history": get_nutrition_history,
}


class Agent:

    def __init__(
        self,
        client: Groq,
        system: str = "",
        tools: list | None = None,
    ):
        self.client = client
        self.system = system
        self.tools = tools or []
        self.messages = []

        if self.system:
            self.messages.append(
                {
                    "role": "system",
                    "content": self.system,
                }
            )

    def __call__(self, message: str = ""):

        if message:
            self.messages.append(
                {
                    "role": "user",
                    "content": message,
                }
            )

        return self.execute()

    def execute(self):

        while True:

            print("Sending request to Groq...")

            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )

            print("Groq response received!")

            response_message = completion.choices[0].message

            # --------------------------------
            # LLM wants to call a tool
            # --------------------------------

            if response_message.tool_calls:

                print("Tool call detected!")

                # Add assistant tool-call message
                self.messages.append(
                    response_message
                )

                for tool_call in response_message.tool_calls:

                    function_name = tool_call.function.name

                    function_args = json.loads(
                        tool_call.function.arguments
                    )

                    print(
                        f"Executing tool: {function_name}"
                    )

                    print(
                        f"Arguments: {function_args}"
                    )

                    function_to_call = TOOL_FUNCTIONS.get(
                        function_name
                    )

                    if function_to_call is None:

                        tool_output = {
                            "error": (
                                f"Unknown tool: {function_name}"
                            )
                        }

                    else:

                        try:

                            function_output = function_to_call(
                                **function_args
                            )

                            tool_output = function_output

                            print(
                                f"Tool output: {function_output}"
                            )

                        except Exception as e:

                            tool_output = {
                                "error": str(e)
                            }

                            print(
                                f"Tool error: {e}"
                            )

                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(
                                tool_output,
                                default=str,
                            ),
                        }
                    )

                # Send tool result back to Groq
                continue

            # --------------------------------
            # Normal final response
            # --------------------------------

            if response_message.content:

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": response_message.content,
                    }
                )

            return response_message.content