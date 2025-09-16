#!/usr/bin/env python3
"""
Simple test script for Gemini AI - just send image and see what comes back
"""

import asyncio
import os
from dotenv import load_dotenv
from app.services.gemini_service import GeminiService

async def test_gemini():
    """Test Gemini AI service with simple image analysis"""
    print("🤖 Testing Gemini AI with Image")
    print("=" * 40)
    
    try:
        # Load environment variables
        load_dotenv("env/config.env")
        load_dotenv()
        
        # Test connection first
        print("🔍 Testing Gemini connection...")
        service = GeminiService()
        
        if service.test_connection():
            print("✅ Gemini connection successful!")
        else:
            print("❌ Gemini connection failed!")
            return False
        
        # Test with sample image
        sample_image_path = "Den_Baas_en_zijn_Madam.jpg"
        if os.path.exists(sample_image_path):
            print(f"\n📸 Sending image to Gemini: {sample_image_path}")
            
            with open(sample_image_path, "rb") as f:
                image_content = f.read()
            
            # Just get raw response from Gemini
            result = await service.parse_bill_image(image_content, "image/jpeg")
            
            print("✅ Gemini responded!")
            print(f"\n📋 Response type: {type(result)}")
            print(f"📋 Response length: {len(str(result))}")
            print("\n📋 Raw response from Gemini:")
            print("-" * 40)
            if isinstance(result, dict):
                print("Response is a dictionary:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            else:
                print(f"Response content: {result}")
            print("-" * 40)
            
            return True
        else:
            print(f"❌ Sample image not found at {sample_image_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini())
    if success:
        print("\n✅ Gemini test completed!")
    else:
        print("\n❌ Gemini test failed!")
