#!/usr/bin/env python3
"""
Test script for Supabase connection
"""

import os
import json
from dotenv import load_dotenv

def test_supabase_connection():
    """Test Supabase connection and credentials"""
    print("🔍 Testing Supabase connection...")
    
    # Load environment variables
    load_dotenv("env/config.env")
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print(f"   SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
    print(f"   SUPABASE_ANON_KEY: {'✅ Set' if supabase_anon_key else '❌ Missing'}")
    print(f"   SUPABASE_SERVICE_KEY: {'✅ Set' if supabase_service_key else '❌ Missing'}")
    
    if not all([supabase_url, supabase_anon_key, supabase_service_key]):
        print("\n❌ Missing Supabase credentials!")
        print("Please add to env/config.env:")
        print("SUPABASE_URL=your_supabase_project_url")
        print("SUPABASE_ANON_KEY=your_supabase_anon_key")
        print("SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key")
        return False
    
    # Test connection with requests
    try:
        import requests
        
        # Test anon key
        headers = {
            "apikey": supabase_anon_key,
            "Authorization": f"Bearer {supabase_anon_key}"
        }
        
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers)
        
        if response.status_code == 200:
            print("✅ Supabase connection successful!")
            return True
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except ImportError:
        print("❌ requests library not available. Install with: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_database_schema():
    """Test if database tables exist"""
    print("\n🗄️ Testing database schema...")
    
    try:
        import requests
        from dotenv import load_dotenv
        
        load_dotenv("env/config.env")
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            print("❌ Supabase credentials not found")
            return False
        
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}"
        }
        
        # Test if bills table exists
        response = requests.get(f"{supabase_url}/rest/v1/bills?select=id&limit=1", headers=headers)
        
        if response.status_code == 200:
            print("✅ Database schema looks good!")
            print("   Tables are accessible")
            return True
        elif response.status_code == 404:
            print("❌ Database schema test failed: Tables not found")
            print("   Please run the schema.sql file in your Supabase SQL Editor")
            print("   Go to: Supabase Dashboard → SQL Editor → New Query")
            return False
        else:
            print(f"❌ Database schema test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            print("   Make sure you've run the schema.sql file in Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Database schema test error: {e}")
        return False

def create_sample_bill_in_db():
    """Create a sample bill in the database"""
    print("\n📝 Creating sample bill in database...")
    
    try:
        import requests
        from dotenv import load_dotenv
        import uuid
        
        load_dotenv("env/config.env")
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_service_key:
            print("❌ Supabase credentials not found")
            return False
        
        headers = {
            "apikey": supabase_service_key,
            "Authorization": f"Bearer {supabase_service_key}",
            "Content-Type": "application/json"
        }
        
        # Create a sample bill
        bill_data = {
            "currency": "EUR",
            "link_token_hash": f"test-token-{uuid.uuid4().hex[:8]}",
            "is_locked": False
        }
        
        response = requests.post(
            f"{supabase_url}/rest/v1/bills",
            headers=headers,
            json=bill_data
        )
        
        print(f"   Bill creation response: {response.status_code}")
        print(f"   Response text: {response.text[:200]}...")
        
        if response.status_code == 201:
            # Check if response has content
            if response.text.strip():
                try:
                    bill = response.json()
                    if isinstance(bill, list) and len(bill) > 0:
                        bill_id = bill[0]['id']
                        print(f"✅ Sample bill created! ID: {bill_id}")
                    else:
                        print("❌ Unexpected response format from Supabase")
                        return False
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON response: {e}")
                    print(f"   Raw response: {response.text}")
                    return False
            else:
                # If response is empty, we need to fetch the created bill
                print("   Response is empty, fetching created bill...")
                
                # Get the bill by link_token_hash
                link_token = bill_data["link_token_hash"]
                fetch_response = requests.get(
                    f"{supabase_url}/rest/v1/bills?link_token_hash=eq.{link_token}&select=id",
                    headers=headers
                )
                
                if fetch_response.status_code == 200 and fetch_response.text.strip():
                    try:
                        bills = fetch_response.json()
                        if isinstance(bills, list) and len(bills) > 0:
                            bill_id = bills[0]['id']
                            print(f"✅ Sample bill created! ID: {bill_id}")
                        else:
                            print("❌ Could not find created bill")
                            return False
                    except json.JSONDecodeError as e:
                        print(f"❌ Failed to parse fetch response: {e}")
                        return False
                else:
                    print("❌ Could not fetch created bill")
                    return False
            
            # Create sample participants
            participants_data = [
                {"bill_id": bill_id, "name": "Alice", "is_payer": True},
                {"bill_id": bill_id, "name": "Bob", "is_payer": False},
                {"bill_id": bill_id, "name": "Charlie", "is_payer": False}
            ]
            
            response = requests.post(
                f"{supabase_url}/rest/v1/participants",
                headers=headers,
                json=participants_data
            )
            
            if response.status_code == 201:
                print("✅ Sample participants created!")
                return bill_id
            else:
                print(f"❌ Failed to create participants: {response.status_code}")
                print(f"   Response: {response.text}")
                return bill_id
        else:
            print(f"❌ Failed to create bill: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating sample bill: {e}")
        return False

def main():
    """Run all Supabase tests"""
    print("🚀 Starting Supabase Tests")
    print("=" * 50)
    
    # Test connection
    if not test_supabase_connection():
        return
    
    # Test database schema
    if not test_database_schema():
        return
    
    # Create sample data
    bill_id = create_sample_bill_in_db()
    
    print("\n" + "=" * 50)
    print("✅ Supabase testing completed!")
    
    if bill_id:
        print(f"\nSample bill ID: {bill_id}")
        print("You can view it in your Supabase dashboard")

if __name__ == "__main__":
    main()
