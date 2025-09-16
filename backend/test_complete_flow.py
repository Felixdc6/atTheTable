#!/usr/bin/env python3
"""
Test script for the complete bill splitting flow
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_complete_flow():
    """Test the complete flow: upload image → parse → create bill → share link"""
    print("🚀 Testing Complete Bill Splitting Flow")
    print("=" * 60)
    
    # Check if sample image exists
    sample_image = Path("Den_Baas_en_zijn_Madam.jpg")
    if not sample_image.exists():
        print("❌ Sample image not found. Using test image...")
        sample_image = Path("sample_bill.jpg")
        if not sample_image.exists():
            print("❌ No sample image found. Please add an image file to test.")
            return False
    
    print(f"📸 Using image: {sample_image}")
    
    # Step 1: Parse bill and create in database
    print("\n1️⃣ Parsing bill and creating in database...")
    try:
        with open(sample_image, "rb") as f:
            files = {"file": (sample_image.name, f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/api/ai/parse-bill", files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Bill parsed and created successfully!")
                bill = result["bill"]
                link_token = result["link_token"]
                print(f"   Bill ID: {bill['id']}")
                print(f"   Link Token: {link_token}")
                print(f"   Items: {len(bill.get('items', []))}")
                print(f"   Currency: {bill.get('currency', 'N/A')}")
            else:
                print("❌ Bill parsing failed:")
                print(f"   Error: {result.get('error', 'Unknown error')}")
                if 'raw_response' in result:
                    print(f"   Raw response: {result['raw_response']}")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing bill: {e}")
        return False
    
    # Step 2: Test public bill access
    print(f"\n2️⃣ Testing public bill access...")
    try:
        response = requests.get(f"{BASE_URL}/api/public/{link_token}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Public bill access successful!")
                bill_data = result["bill"]
                print(f"   Items available: {len(bill_data.get('items', []))}")
                print(f"   Participants: {len(bill_data.get('participants', []))}")
            else:
                print("❌ Public bill access failed")
                return False
        else:
            print(f"❌ Public access error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing public bill: {e}")
        return False
    
    # Step 3: Create participants
    print(f"\n3️⃣ Creating participants...")
    participants = ["Alice", "Bob", "Charlie"]
    participant_ids = []
    
    for name in participants:
        try:
            response = requests.post(
                f"{BASE_URL}/api/public/{link_token}/participant",
                params={"name": name, "is_payer": name == "Alice"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    participant_id = result["participant"]["id"]
                    participant_ids.append(participant_id)
                    print(f"✅ Created participant: {name} (ID: {participant_id})")
                else:
                    print(f"❌ Failed to create participant: {name}")
                    return False
            else:
                print(f"❌ Error creating participant {name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating participant {name}: {e}")
            return False
    
    # Step 4: Test claiming items
    print(f"\n4️⃣ Testing item claiming...")
    
    # Get the bill again to see items
    try:
        response = requests.get(f"{BASE_URL}/api/public/{link_token}")
        if response.status_code == 200:
            result = response.json()
            bill_data = result["bill"]
            items = bill_data.get("items", [])
            
            if items:
                # Test exclusive claim
                first_item = items[0]
                item_id = first_item["id"]
                participant_id = participant_ids[0]  # Alice
                
                claim_data = {
                    "item_id": item_id,
                    "participant_id": participant_id,
                    "quantity": 1
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/public/{link_token}/claim-exclusive",
                    json=claim_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print(f"✅ Successfully claimed item: {first_item['name']}")
                        print(f"   Remaining quantity: {result.get('remaining_quantity', 'N/A')}")
                    else:
                        print("❌ Claim failed")
                        return False
                else:
                    print(f"❌ Claim error: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
            else:
                print("❌ No items found to claim")
                return False
        else:
            print("❌ Could not retrieve bill for claiming")
            return False
            
    except Exception as e:
        print(f"❌ Error testing claims: {e}")
        return False
    
    # Step 5: Test shared pool
    print(f"\n5️⃣ Testing shared pool...")
    
    if len(items) > 1 and len(participant_ids) > 1:
        second_item = items[1]
        item_id = second_item["id"]
        
        # Check remaining quantity first
        remaining = second_item.get("qty_total", 1)  # Use total quantity as fallback
        pool_size = min(2, remaining)  # Use smaller of 2 or remaining quantity
        
        print(f"   Item: {second_item['name']}, Remaining: {remaining}, Pool size: {pool_size}")
        
        # Initialize shared pool
        shared_init_data = {
            "item_id": item_id,
            "participant_id": participant_ids[0],  # Alice
            "pool_size": pool_size
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/public/{link_token}/shared-init",
                json=shared_init_data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"✅ Initialized shared pool for: {second_item['name']}")
                    print(f"   Pool size: {result.get('pool_size', 'N/A')}")
                    
                    # Bob joins the shared pool
                    shared_join_data = {
                        "item_id": item_id,
                        "participant_id": participant_ids[1]  # Bob
                    }
                    
                    response = requests.post(
                        f"{BASE_URL}/api/public/{link_token}/shared-join",
                        json=shared_join_data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            print(f"✅ Bob joined shared pool")
                            print(f"   Total members: {result.get('total_members', 'N/A')}")
                        else:
                            print("❌ Failed to join shared pool")
                            return False
                    else:
                        print(f"❌ Join shared pool error: {response.status_code}")
                        return False
                else:
                    print("❌ Failed to initialize shared pool")
                    return False
            else:
                print(f"❌ Shared pool init error: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing shared pool: {e}")
            return False
    else:
        print("⚠️ Skipping shared pool test (not enough items or participants)")
    
    print("\n" + "=" * 60)
    print("✅ Complete flow test successful!")
    print(f"\n🔗 Share this link with participants:")
    print(f"   {BASE_URL}/api/public/{link_token}")
    
    return True

def main():
    """Run the complete flow test"""
    print("🧪 Starting Complete Flow Test")
    print("Make sure the API server is running: python main.py")
    print()
    
    success = test_complete_flow()
    
    if success:
        print("\n🎉 All tests passed! The bill splitting system is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
