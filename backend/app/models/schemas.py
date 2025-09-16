from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from decimal import Decimal
from datetime import datetime
from uuid import UUID

# Enums
from enum import Enum

class ItemCategory(str, Enum):
    FOOD = "Food"
    DRINKS = "Drinks"

class ItemType(str, Enum):
    ITEM = "item"
    SURCHARGE = "surcharge"

# Base models
class VendorInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    datetime: Optional[datetime] = None

class BillMeta(BaseModel):
    subtotal: Optional[float] = None
    service: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None

class ItemBase(BaseModel):
    name: str
    category: ItemCategory
    unit_price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=1)
    type: ItemType = ItemType.ITEM
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    notes: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: UUID
    bill_id: UUID
    qty_total: int
    qty_shared_pool: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

# Gemini API response models
class GeminiBillResponse(BaseModel):
    vendor: VendorInfo
    currency: str = "EUR"
    items: List[ItemCreate]
    meta: BillMeta

# Bill models
class BillCreate(BaseModel):
    currency: str = "EUR"

class BillResponse(BaseModel):
    id: UUID
    creator_id: Optional[UUID] = None
    currency: str
    link_token_hash: str
    created_at: datetime
    updated_at: datetime
    is_locked: bool = False

    class Config:
        from_attributes = True

class BillWithItems(BillResponse):
    items: List[ItemResponse] = []
    participants: List['ParticipantResponse'] = []

# Participant models
class ParticipantCreate(BaseModel):
    name: str
    is_payer: bool = False

class ParticipantResponse(BaseModel):
    id: UUID
    bill_id: UUID
    name: str
    is_payer: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Claim models
class ClaimCreate(BaseModel):
    item_id: UUID
    participant_id: UUID
    qty_claimed: int = Field(..., ge=1)

class ClaimResponse(BaseModel):
    id: UUID
    bill_id: UUID
    item_id: UUID
    participant_id: UUID
    qty_claimed: int
    created_at: datetime

    class Config:
        from_attributes = True

# Shared pool models
class SharedPoolInit(BaseModel):
    item_id: UUID
    participant_id: UUID
    pool_size: int = Field(..., ge=1)

class SharedPoolJoin(BaseModel):
    item_id: UUID
    participant_id: UUID

class SharedMemberResponse(BaseModel):
    id: UUID
    item_id: UUID
    participant_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Public API models
class PublicBillResponse(BaseModel):
    id: UUID
    currency: str
    items: List[ItemResponse]
    participants: List[ParticipantResponse]
    is_locked: bool

class PublicClaimRequest(BaseModel):
    item_id: UUID
    participant_id: UUID
    quantity: int = Field(..., ge=1)

class PublicSharedInitRequest(BaseModel):
    item_id: UUID
    participant_id: UUID
    pool_size: int = Field(..., ge=1)

class PublicSharedJoinRequest(BaseModel):
    item_id: UUID
    participant_id: UUID

# Results models
class ParticipantTotal(BaseModel):
    participant_id: UUID
    participant_name: str
    exclusive_total: Decimal
    shared_total: Decimal
    grand_total: Decimal

class BillResults(BaseModel):
    bill_id: UUID
    participants: List[ParticipantTotal]
    total_bill: Decimal
    currency: str

# Update forward references
BillWithItems.model_rebuild()
