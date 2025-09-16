#!/usr/bin/env python3
"""
Test script for the FastAPI backend
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test basic API connectivity"""
    print("🔍 Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running?")
        print("   Run: python main.py")
        return False

def test_health_endpoint():
    """Test health check endpoint"""
    print("\n🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_ai_health():
    """Test AI service health"""
    print("\n🤖 Testing AI service...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai/health")
        if response.status_code == 200:
            print("✅ AI service is healthy!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ AI service error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI service error: {e}")
        return False

def test_public_endpoints():
    """Test public API endpoints"""
    print("\n🌐 Testing public endpoints...")
    
    # Test get bill endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/public/test-token")
        print(f"   GET /api/public/test-token: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test claim exclusive endpoint
    try:
        data = {"item_id": "test-item", "participant_id": "test-participant", "quantity": 1}
        response = requests.post(f"{BASE_URL}/api/public/test-token/claim-exclusive", json=data)
        print(f"   POST /api/public/test-token/claim-exclusive: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")

def test_bill_parsing():
    """Test bill parsing with sample image"""
    print("\n📄 Testing bill parsing...")
    
    # Check if sample image exists
    sample_image = Path("sample_bill.jpg")
    if not sample_image.exists():
        print("❌ No sample image found. Create a sample_bill.jpg file to test parsing.")
        return False
    
    try:
        with open(sample_image, "rb") as f:
            files = {"file": ("sample_bill.jpg", f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/api/ai/parse-bill", files=files)
        
        if response.status_code == 200:
            print("✅ Bill parsing successful!")
            result = response.json()
            print(f"   Parsed {len(result.get('items', []))} items")
            return True
        else:
            print(f"❌ Bill parsing failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Bill parsing error: {e}")
        return False

def create_sample_bill_data():
    """Create sample bill data for testing"""
    print("\n📊 Creating sample bill data...")
    
    sample_bill = {
        "vendor": {
            "name": "Trattoria Roma",
            "address": "123 Main St, Rome",
            "datetime": "2025-01-09T20:41:00Z"
        },
        "currency": "EUR",
        "items": [
            {
                "name": "Margherita Pizza",
                "category": "Food",
                "unit_price": 12.50,
                "quantity": 2,
                "type": "item",
                "confidence": 0.96,
                "notes": None
            },
            {
                "name": "Coca Cola",
                "category": "Drinks",
                "unit_price": 3.00,
                "quantity": 3,
                "type": "item",
                "confidence": 0.98,
                "notes": None
            },
            {
                "name": "Service Charge",
                "category": "Food",
                "unit_price": 6.00,
                "quantity": 1,
                "type": "surcharge",
                "confidence": 0.90,
                "notes": "10%"
            }
        ],
        "meta": {
            "subtotal": 33.50,
            "service": 6.00,
            "tax": None,
            "total": 39.50
        }
    }
    
    # Save sample data
    with open("sample_bill_data.json", "w") as f:
        json.dump(sample_bill, f, indent=2)
    
    print("✅ Sample bill data created: sample_bill_data.json")
    return sample_bill

def main():
    """Run all tests"""
    print("🚀 Starting API Tests")
    print("=" * 50)
    
    # Test basic connectivity
    if not test_api_connection():
        return
    
    # Test health endpoints
    test_health_endpoint()
    test_ai_health()
    
    # Test public endpoints
    test_public_endpoints()
    
    # Test bill parsing
    test_bill_parsing()
    
    # Create sample data
    create_sample_bill_data()
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")
    print("\nNext steps:")
    print("1. Set up Supabase project")
    print("2. Add Supabase credentials to config.env")
    print("3. Test database connection")

if __name__ == "__main__":
    main()
