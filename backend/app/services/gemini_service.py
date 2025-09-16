from google import genai
import os
from dotenv import load_dotenv
from typing import Union, BinaryIO
import json

class GeminiService:
    """
    Service for processing bill images using Google's Gemini AI.
    Takes an image as input and returns parsed bill data in JSON format.
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv("env/config.env")
        
        # Get API key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize client with API key
        self.client = genai.Client(api_key=self.api_key)
    
    def parse_bill_image(self, image_path: str) -> dict:
        """
        Parse a bill image and return structured JSON data.
        
        Args:
            image_path (str): Path to the image file to process
            
        Returns:
            dict: Parsed bill data in JSON format
        """
        # Upload the image file to Gemini
        file_ref = self.client.files.upload(file=image_path)
        
        # Generate content using the uploaded image
        resp = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=["what has been ordered on the bill? Group: Drinks, Food. Show unit prices in euros.Return in json format.", file_ref],
        )
        
        # Parse the response text as JSON
        try:
            # Clean the response text (remove markdown code blocks)
            cleaned_text = resp.text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            raw_data = json.loads(cleaned_text)
            # Transform the response to match our expected format
            return self._transform_gemini_response(raw_data)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw text wrapped in a structure
            return {"raw_response": resp.text, "error": f"Failed to parse JSON response: {str(e)}"}
    
    def parse_bill_from_bytes(self, image_bytes: bytes, filename: str = "bill.jpg") -> dict:
        """
        Parse a bill image from bytes and return structured JSON data.
        
        Args:
            image_bytes (bytes): Image data as bytes
            filename (str): Name for the temporary file
            
        Returns:
            dict: Parsed bill data in JSON format
        """
        import tempfile
        
        # Create a temporary file to store the image bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.split('.')[-1]}") as temp_file:
            temp_file.write(image_bytes)
            temp_path = temp_file.name
        
        try:
            # Parse the temporary file
            result = self.parse_bill_image(temp_path)
            return result
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def _transform_gemini_response(self, raw_data: dict) -> dict:
        """
        Transform Gemini response to match our expected schema
        """
        items = []
        
        # Process Drinks
        if "Drinks" in raw_data:
            for drink in raw_data["Drinks"]:
                items.append({
                    "name": drink.get("item", ""),
                    "category": "Drinks",
                    "unit_price": float(drink.get("unit_price_eur", drink.get("unit_price_euros", 0))),
                    "quantity": int(drink.get("quantity", 1)),
                    "type": "item",
                    "confidence": 0.95,
                    "notes": None
                })
        
        # Process Food
        if "Food" in raw_data:
            for food in raw_data["Food"]:
                items.append({
                    "name": food.get("item", ""),
                    "category": "Food",
                    "unit_price": float(food.get("unit_price_eur", food.get("unit_price_euros", 0))),
                    "quantity": int(food.get("quantity", 1)),
                    "type": "item",
                    "confidence": 0.95,
                    "notes": None
                })
        
        # Calculate totals
        subtotal = sum(item["unit_price"] * item["quantity"] for item in items)
        
        return {
            "vendor": {
                "name": None,
                "address": None,
                "datetime": None
            },
            "currency": "EUR",
            "items": items,
            "meta": {
                "subtotal": float(subtotal),
                "service": None,
                "tax": None,
                "total": float(subtotal)
            }
        }
