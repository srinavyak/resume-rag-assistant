import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found — check your .env file")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say hello in one short sentence.",
)
print(response.text)



# //To get available models list that supports from gemini
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)