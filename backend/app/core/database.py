import os
import hashlib
import secrets
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv("env/config.env")

class DatabaseService:
    """Service for interacting with Supabase database"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.supabase_url or not self.supabase_service_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_service_key)
    
    def generate_link_token(self) -> str:
        """Generate a secure random token for bill sharing"""
        return secrets.token_urlsafe(32)
    
    def hash_token(self, token: str) -> str:
        """Hash a token for secure storage"""
        return hashlib.sha256(token.encode()).hexdigest()
    
    # Bill operations
    def create_bill(self, currency: str = "EUR") -> Dict[str, Any]:
        """Create a new bill and return it with the unhashed token"""
        token = self.generate_link_token()
        token_hash = self.hash_token(token)
        
        bill_data = {
            "currency": currency,
            "link_token_hash": token_hash,
            "is_locked": False
        }
        
        result = self.client.table("bills").insert(bill_data).execute()
        
        if result.data:
            bill = result.data[0]
            bill["link_token"] = token  # Include unhashed token for response
            return bill
        else:
            raise Exception("Failed to create bill")
    
    def get_bill_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get bill by unhashed token"""
        token_hash = self.hash_token(token)
        
        result = self.client.table("bills").select("*").eq("link_token_hash", token_hash).execute()
        
        if result.data:
            return result.data[0]
        return None
    
    def get_bill_with_items(self, bill_id: str) -> Optional[Dict[str, Any]]:
        """Get bill with all related items and participants"""
        # Get bill
        bill_result = self.client.table("bills").select("*").eq("id", bill_id).execute()
        if not bill_result.data:
            return None
        
        bill = bill_result.data[0]
        
        # Get items
        items_result = self.client.table("items").select("*").eq("bill_id", bill_id).execute()
        bill["items"] = items_result.data or []
        
        # Get participants
        participants_result = self.client.table("participants").select("*").eq("bill_id", bill_id).execute()
        bill["participants"] = participants_result.data or []
        
        return bill
    
    def update_bill(self, bill_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update bill fields"""
        result = self.client.table("bills").update(updates).eq("id", bill_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to update bill")
    
    # Item operations
    def create_items(self, bill_id: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple items for a bill"""
        try:
            created_items = []
            
            # Create items one by one to avoid batch issues
            for item in items:
                db_item = {
                    "bill_id": bill_id,
                    "name": item.get("name", ""),
                    "category": item.get("category", "Food"),
                    "unit_price": float(item.get("unit_price", 0)),
                    "qty_total": int(item.get("quantity", 1)),
                    "type": item.get("type", "item"),
                    "confidence": float(item.get("confidence", 1.0)),
                    "notes": item.get("notes")
                }
                
                result = self.client.table("items").insert(db_item).execute()
                
                if result.data:
                    created_items.append(result.data[0])
                else:
                    print(f"Failed to create item: {db_item}")
            
            return created_items
        except Exception as e:
            print(f"Error creating items: {e}")
            print(f"Items data: {items}")
            raise Exception(f"Failed to create items: {str(e)}")
    
    def get_items(self, bill_id: str) -> List[Dict[str, Any]]:
        """Get all items for a bill"""
        result = self.client.table("items").select("*").eq("bill_id", bill_id).execute()
        return result.data or []
    
    def update_item(self, item_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an item"""
        result = self.client.table("items").update(updates).eq("id", item_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to update item")
    
    # Participant operations
    def create_participants(self, bill_id: str, participants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple participants for a bill"""
        for participant in participants:
            participant["bill_id"] = bill_id
        
        result = self.client.table("participants").insert(participants).execute()
        
        if result.data:
            return result.data
        else:
            raise Exception("Failed to create participants")
    
    def get_participants(self, bill_id: str) -> List[Dict[str, Any]]:
        """Get all participants for a bill"""
        result = self.client.table("participants").select("*").eq("bill_id", bill_id).execute()
        return result.data or []
    
    def create_participant(self, bill_id: str, name: str, is_payer: bool = False) -> Dict[str, Any]:
        """Create a single participant"""
        participant_data = {
            "bill_id": bill_id,
            "name": name,
            "is_payer": is_payer
        }
        
        result = self.client.table("participants").insert(participant_data).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to create participant")
    
    # Claim operations
    def create_claim(self, bill_id: str, item_id: str, participant_id: str, qty_claimed: int) -> Dict[str, Any]:
        """Create an exclusive claim"""
        claim_data = {
            "bill_id": bill_id,
            "item_id": item_id,
            "participant_id": participant_id,
            "qty_claimed": qty_claimed
        }
        
        result = self.client.table("claims").insert(claim_data).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to create claim")
    
    def get_claims(self, bill_id: str) -> List[Dict[str, Any]]:
        """Get all claims for a bill"""
        result = self.client.table("claims").select("*").eq("bill_id", bill_id).execute()
        return result.data or []
    
    def delete_claim(self, claim_id: str) -> bool:
        """Delete a claim"""
        result = self.client.table("claims").delete().eq("id", claim_id).execute()
        return True
    
    # Shared pool operations
    def init_shared_pool(self, item_id: str, participant_id: str, pool_size: int) -> Dict[str, Any]:
        """Initialize a shared pool for an item"""
        # First, update the item with the pool size
        self.client.table("items").update({"qty_shared_pool": pool_size}).eq("id", item_id).execute()
        
        # Then add the participant to the shared members
        member_data = {
            "item_id": item_id,
            "participant_id": participant_id
        }
        
        result = self.client.table("shared_members").insert(member_data).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to initialize shared pool")
    
    def join_shared_pool(self, item_id: str, participant_id: str) -> Dict[str, Any]:
        """Join an existing shared pool"""
        member_data = {
            "item_id": item_id,
            "participant_id": participant_id
        }
        
        result = self.client.table("shared_members").insert(member_data).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise Exception("Failed to join shared pool")
    
    def leave_shared_pool(self, item_id: str, participant_id: str) -> bool:
        """Leave a shared pool"""
        result = self.client.table("shared_members").delete().eq("item_id", item_id).eq("participant_id", participant_id).execute()
        return True
    
    def get_shared_members(self, item_id: str) -> List[Dict[str, Any]]:
        """Get all shared members for an item"""
        result = self.client.table("shared_members").select("*").eq("item_id", item_id).execute()
        return result.data or []
    
    # Results and calculations
    def get_participant_totals(self, bill_id: str) -> List[Dict[str, Any]]:
        """Get calculated totals for all participants"""
        try:
            result = self.client.rpc("get_participant_totals", {"bill_uuid": bill_id}).execute()
            return result.data or []
        except Exception:
            # Fallback: return empty list for now
            # This would need a more complex manual calculation
            return []
    
    def get_remaining_quantity(self, item_id: str) -> int:
        """Get remaining quantity for an item"""
        try:
            result = self.client.rpc("calculate_remaining_qty", {"item_uuid": item_id}).execute()
            return result.data or 0
        except Exception:
            # Fallback: calculate manually
            # Get item total quantity
            item_result = self.client.table("items").select("qty_total").eq("id", item_id).execute()
            if not item_result.data:
                return 0
            
            total_qty = item_result.data[0]["qty_total"]
            
            # Get exclusive claims
            claims_result = self.client.table("claims").select("qty_claimed").eq("item_id", item_id).execute()
            exclusive_claimed = sum(claim["qty_claimed"] for claim in claims_result.data or [])
            
            # Get shared pool quantity
            item_result = self.client.table("items").select("qty_shared_pool").eq("id", item_id).execute()
            shared_pool = item_result.data[0]["qty_shared_pool"] if item_result.data else 0
            
            return total_qty - exclusive_claimed - shared_pool
