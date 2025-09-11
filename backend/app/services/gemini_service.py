import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from google import genai
from PIL import Image
import io

class GeminiService:
    """Service for handling Gemini AI operations"""
    
    def __init__(self):
        # Load environment variables from multiple sources
        load_dotenv("env/config.env")  # Local config file
        load_dotenv()  # System environment variables
        
        # Get API key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in:\n"
                "1. env/config.env file, or\n"
                "2. System environment variables"
            )
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        # System prompt for bill parsing
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT", 
            """You are an assistant that extracts line items from restaurant receipts.
Return ONLY JSON matching the schema.

- Identify line items (name, category Food/Drinks, unit_price, quantity)
- Ignore totals, change due
- Merge duplicates by name
- Service charge/tax as type="surcharge"
- Confidence score per item
- Return valid JSON only"""
        )
    
    async def parse_bill_image(self, image_content: bytes, content_type: str) -> Dict[str, Any]:
        """
        Parse a bill image using Gemini AI
        """
        try:
            # Upload image to Gemini
            file_ref = self.client.files.upload(
                file=io.BytesIO(image_content),
                mime_type=content_type
            )
            
            # Generate content with system prompt and image
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[self.system_prompt, file_ref]
            )
            
            # Parse JSON response
            result = json.loads(response.text)
            
            # Validate the response structure
            self._validate_bill_structure(result)
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from Gemini: {e}")
        except Exception as e:
            raise Exception(f"Error parsing bill with Gemini: {e}")
    
    def _validate_bill_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate that the parsed bill has the expected structure
        """
        required_fields = ["vendor", "currency", "items", "meta"]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate items structure
        if not isinstance(data["items"], list):
            raise ValueError("Items must be a list")
        
        for item in data["items"]:
            if not all(key in item for key in ["name", "category", "unit_price", "quantity", "type"]):
                raise ValueError("Invalid item structure")
    
    def test_connection(self) -> bool:
        """
        Test if Gemini service is working
        """
        try:
            # Simple test with text
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents="Hello, respond with 'OK' if you can read this."
            )
            return "OK" in response.text
        except Exception:
            return False
