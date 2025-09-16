#!/usr/bin/env python3
"""
Quick test script for the API without external dependencies
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    print("🚀 Quick API Test")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: AI health endpoint
    print("\n3. Testing AI health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/ai/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Public endpoint
    print("\n4. Testing public endpoint...")
    try:
        response = requests.get(f"{base_url}/api/public/test-token")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 30)
    print("✅ Quick test completed!")

if __name__ == "__main__":
    test_api()
