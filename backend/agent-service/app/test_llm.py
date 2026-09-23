from app.ai_agent.client import client


print("Sending request to Groq...")


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Hello, reply with only: Hello"
        }
    ],
    max_tokens=20,
)


print("Response received!")

print(response.choices[0].message)