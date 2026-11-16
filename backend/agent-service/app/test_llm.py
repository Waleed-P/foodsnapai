from app.client import get_groq_client
from app.core.config import settings

client = get_groq_client()

if __name__ == "__main__":
    print("Sending test request to Groq...")
    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "user", "content": "Hello, reply with only: Hello"}
            ],
            max_tokens=20,
        )
        print("Response received:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error testing Groq client: {e}")
