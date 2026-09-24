
#script to find which models are avaiable under the free tier api key of google ai studio

import os
from google import genai

# Read key from environment variable
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not api_key:
    # Or replace with your hardcoded API key string for testing:
    api_key = "AQ.Ab8RN6JCTUdflpQimAyYUAYqL0hrOxrSsHcL-YHHg3s8XTjifA"

client = genai.Client(api_key=api_key)

print("--- Available Models ---")
for m in client.models.list():
    print(m.name)