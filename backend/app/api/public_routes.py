from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.database import DatabaseService
from app.models.schemas import PublicClaimRequest, PublicSharedInitRequest, PublicSharedJoinRequest

router = APIRouter()

@router.get("/{token}")
async def get_bill(token: str):
    """
    Get bill details by public token (no authentication required)
    """
    try:
        db_service = DatabaseService()
        bill = db_service.get_bill_by_token(token)
        
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        # Get bill with items and participants
        complete_bill = db_service.get_bill_with_items(bill["id"])
        
        if not complete_bill:
            raise HTTPException(status_code=404, detail="Bill data not found")
        
        return {
            "success": True,
            "bill": complete_bill
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bill: {str(e)}")

@router.post("/{token}/claim-exclusive")
async def claim_exclusive(token: str, request: PublicClaimRequest):
    """
    Claim exclusive items (I had this)
    """
    try:
        db_service = DatabaseService()
        
        # Get bill by token
        bill = db_service.get_bill_by_token(token)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        bill_id = bill["id"]
        
        # Check if item exists and has enough quantity
        items = db_service.get_items(bill_id)
        item = next((i for i in items if str(i["id"]) == str(request.item_id)), None)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check remaining quantity
        remaining = db_service.get_remaining_quantity(request.item_id)
        if remaining < request.quantity:
            raise HTTPException(status_code=400, detail="Not enough quantity available")
        
        # Create the claim
        claim = db_service.create_claim(
            bill_id=bill_id,
            item_id=str(request.item_id),
            participant_id=str(request.participant_id),
            qty_claimed=request.quantity
        )
        
        return {
            "success": True,
            "claim": claim,
            "remaining_quantity": remaining - request.quantity
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating claim: {str(e)}")

@router.post("/{token}/shared-init")
async def init_shared_pool(token: str, request: PublicSharedInitRequest):
    """
    Initialize a shared pool for an item
    """
    try:
        db_service = DatabaseService()
        
        # Get bill by token
        bill = db_service.get_bill_by_token(token)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        bill_id = bill["id"]
        
        # Check if item exists
        items = db_service.get_items(bill_id)
        item = next((i for i in items if str(i["id"]) == str(request.item_id)), None)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Check if pool size is valid
        remaining = db_service.get_remaining_quantity(request.item_id)
        if remaining < request.pool_size:
            raise HTTPException(status_code=400, detail="Pool size exceeds available quantity")
        
        # Initialize shared pool
        shared_member = db_service.init_shared_pool(
            item_id=str(request.item_id),
            participant_id=str(request.participant_id),
            pool_size=request.pool_size
        )
        
        return {
            "success": True,
            "shared_pool": shared_member,
            "pool_size": request.pool_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing shared pool: {str(e)}")

@router.post("/{token}/shared-join")
async def join_shared_pool(token: str, request: PublicSharedJoinRequest):
    """
    Join an existing shared pool
    """
    try:
        db_service = DatabaseService()
        
        # Get bill by token
        bill = db_service.get_bill_by_token(token)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        # Check if shared pool exists
        shared_members = db_service.get_shared_members(str(request.item_id))
        if not shared_members:
            raise HTTPException(status_code=404, detail="Shared pool not found")
        
        # Join the shared pool
        shared_member = db_service.join_shared_pool(
            item_id=str(request.item_id),
            participant_id=str(request.participant_id)
        )
        
        return {
            "success": True,
            "shared_member": shared_member,
            "total_members": len(shared_members) + 1
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error joining shared pool: {str(e)}")

@router.post("/{token}/shared-leave")
async def leave_shared_pool(token: str, request: PublicSharedJoinRequest):
    """
    Leave a shared pool
    """
    try:
        db_service = DatabaseService()
        
        # Get bill by token
        bill = db_service.get_bill_by_token(token)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        # Leave the shared pool
        success = db_service.leave_shared_pool(
            item_id=str(request.item_id),
            participant_id=str(request.participant_id)
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Not a member of this shared pool")
        
        return {
            "success": True,
            "message": "Left shared pool successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leaving shared pool: {str(e)}")

@router.post("/{token}/participant")
async def create_participant(token: str, name: str, is_payer: bool = False):
    """
    Create a new participant for the bill
    """
    try:
        db_service = DatabaseService()
        
        # Get bill by token
        bill = db_service.get_bill_by_token(token)
        if not bill:
            raise HTTPException(status_code=404, detail="Bill not found")
        
        # Create participant
        participant = db_service.create_participant(
            bill_id=bill["id"],
            name=name,
            is_payer=is_payer
        )
        
        return {
            "success": True,
            "participant": participant
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating participant: {str(e)}")
