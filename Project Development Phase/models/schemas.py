from pydantic import BaseModel
from typing import Optional, List

class HomeBudgetInput(BaseModel):
    total_budget: float
    living_room: bool = False
    kitchen: bool = False
    bedroom: bool = False
    num_lights: int = 0
    num_fans: int = 0
    num_furniture: int = 0
    num_dining_tables: int = 0
    additional_requirements: Optional[str] = None

class PartyBudgetInput(BaseModel):
    total_budget: float
    party_type: str
    num_guests: int
    venue_type: Optional[str] = None
    needs_catering: bool = False
    needs_decoration: bool = False
    needs_entertainment: bool = False
    additional_requirements: Optional[str] = None

class JewelryBudgetInput(BaseModel):
    total_budget: float
    occasion: str
    preferences: Optional[str] = None
    # Note: image_path will be handled separately in the route via Form/UploadFile data