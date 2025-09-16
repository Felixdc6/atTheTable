#!/usr/bin/env python3
"""
Create a sample receipt image for testing Gemini integration
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_receipt():
    """Create a sample restaurant receipt image"""
    print("📄 Creating sample receipt image...")
    
    # Create image
    width, height = 400, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font_large = ImageFont.truetype("arial.ttf", 20)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw receipt content
    y_position = 20
    
    # Restaurant name
    draw.text((width//2 - 80, y_position), "TRATTORIA ROMA", fill='black', font=font_large)
    y_position += 40
    
    # Address
    draw.text((width//2 - 100, y_position), "123 Main Street, Rome", fill='black', font=font_small)
    y_position += 30
    
    # Date
    draw.text((width//2 - 80, y_position), "2025-01-09 20:41", fill='black', font=font_small)
    y_position += 40
    
    # Items
    items = [
        ("Margherita Pizza", "12.50", "2"),
        ("Coca Cola", "3.00", "3"),
        ("Tiramisu", "6.50", "1"),
        ("", "", ""),
        ("Subtotal", "33.50", ""),
        ("Service Charge", "6.00", ""),
        ("", "", ""),
        ("TOTAL", "39.50", "")
    ]
    
    for item, price, qty in items:
        if item:  # Skip empty lines
            draw.text((20, y_position), item, fill='black', font=font_medium)
            if qty:
                draw.text((200, y_position), f"x{qty}", fill='black', font=font_medium)
            if price:
                draw.text((width - 80, y_position), f"€{price}", fill='black', font=font_medium)
        y_position += 25
    
    # Save image
    image.save("sample_bill.jpg", "JPEG", quality=95)
    print("✅ Sample receipt created: sample_bill.jpg")
    
    return "sample_bill.jpg"

def main():
    """Create sample receipt image"""
    print("🚀 Creating Sample Receipt Image")
    print("=" * 40)
    
    image_path = create_sample_receipt()
    
    print(f"\n✅ Sample image ready: {image_path}")
    print("You can now test the bill parsing API with this image!")

if __name__ == "__main__":
    main()
