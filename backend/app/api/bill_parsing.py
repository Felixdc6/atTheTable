from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any
import json
from app.services.gemini_service import GeminiService
from app.core.database import DatabaseService
from app.models.schemas import GeminiBillResponse, BillResponse, BillWithItems

router = APIRouter()

@router.post("/parse-bill")
async def parse_bill(file: UploadFile = File(...)):
    """
    Parse a bill image using Gemini AI and create a bill in the database
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        # Initialize services
        gemini_service = GeminiService()
        db_service = DatabaseService()
        
        # Parse the bill with Gemini
        gemini_result = gemini_service.parse_bill_from_bytes(content, file.filename)
        
        # Validate the Gemini response
        try:
            parsed_bill = GeminiBillResponse(**gemini_result)
        except Exception as e:
            # If JSON parsing fails, return the raw response
            return {
                "success": False,
                "raw_response": gemini_result,
                "error": f"Failed to parse Gemini response: {str(e)}"
            }
        
        # Create bill in database
        bill = db_service.create_bill(currency=parsed_bill.currency)
        bill_id = bill["id"]
        
        # Create items in database
        items = db_service.create_items(bill_id, [item.dict() for item in parsed_bill.items])
        
        # Get the complete bill with items
        complete_bill = db_service.get_bill_with_items(bill_id)
        
        return {
            "success": True,
            "bill": complete_bill,
            "link_token": bill["link_token"],  # Include the unhashed token for sharing
            "parsed_data": parsed_bill.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing bill: {str(e)}")

@router.get("/health")
async def ai_health():
    """Check if AI service is working"""
    try:
        gemini_service = GeminiService()
        return {"status": "healthy", "service": "gemini"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
