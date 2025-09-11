from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("env/config.env")

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize client with API key
client = genai.Client(api_key=api_key)

# Generate content
from google import genai

client = genai.Client()
file_ref = client.files.upload(file="Den_Baas_en_zijn_Madam.jpg")  # stores for ~48h

resp = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=["what has been ordered on the bill? Group: Drinks, Food. Show unit prices in euros.Return in json format.", file_ref],
)
print(resp.text)
