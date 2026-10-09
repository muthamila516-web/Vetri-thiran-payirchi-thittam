import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(f"Loaded Key: {api_key[:10]}...")

genai.configure(api_key=api_key)
# Updated to the latest available model from the error log
model = genai.GenerativeModel("gemini-3.8-flash")

try:
    response = model.generate_content("Say hello")
    print("AI Response:", response.text)
    print("API Key is working perfectly! 🎉")
except Exception as e:
    print("API Error Details:", str(e))