import os
from huggingface_hub import InferenceClient
from groq import Groq
API_KEY=os.environ["API_KEY"]
client = Groq(
    api_key=API_KEY
)




# client = InferenceClient(
#     api_key=HF_TOKEN,
#     model="meta-llama/Llama-3.3-70B-Instruct"
# )