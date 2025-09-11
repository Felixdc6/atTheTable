from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any
import json
from app.services.gemini_service import GeminiService

router = APIRouter()

@router.post("/parse-bill")
async def parse_bill(file: UploadFile = File(...)):
    """
    Parse a bill image using Gemini AI and return structured JSON
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        content = await file.read()
        
        # Initialize Gemini service
        gemini_service = GeminiService()
        
        # Parse the bill
        result = await gemini_service.parse_bill_image(content, file.content_type)
        
        return result
        
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
