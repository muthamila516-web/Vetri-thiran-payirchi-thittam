from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from typing import Optional
from datetime import datetime
import os
import shutil
import urllib.parse
from models.schemas import HomeBudgetInput, PartyBudgetInput, JewelryBudgetInput

router = APIRouter()

def save_upload_file(upload_file: UploadFile) -> str:
    """Helper function to save uploaded images locally for jewelry analysis."""
    os.makedirs("static/uploads", exist_ok=True)
    file_path = f"static/uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{upload_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path


# 1. HOME INTERIOR PLANNER ROUTE
@router.post("/home-budget")
def plan_home_budget(budget_input: HomeBudgetInput, request: Request):
    total_b = float(budget_input.total_budget or 50000)
    num_l = int(budget_input.num_lights or 4)
    num_f = int(budget_input.num_fans or 2)
    num_furn = int(budget_input.num_furniture or 2)

    alloc_light = int(total_b * 0.25)
    alloc_fan = int(total_b * 0.25)
    alloc_furn = int(total_b - (alloc_light + alloc_fan))

    return {
        "total_budget": total_b,
        "remaining_budget": 0,
        "recommendation_type": "home",
        "timestamp": datetime.utcnow().isoformat(),
        "budget_breakdown": [
            {
                "category": "Lighting & Electricals",
                "allocation": alloc_light,
                "items": [
                    {
                        "name": "Philips Smart LED Downlights",
                        "description": "Warm White Recessed Panel Lights",
                        "estimated_price": int(alloc_light / max(1, num_l)),
                        "quantity": num_l,
                        "search_terms": "philips led downlight",
                        "shopping_links": {
                            "amazon": "https://www.amazon.in/s?k=philips+led+downlight",
                            "flipkart": "https://www.flipkart.com/search?q=philips+led+downlight",
                            "ikea": "https://www.ikea.com/in/en/search/?q=philips+led+downlight"
                        }
                    }
                ]
            },
            {
                "category": "Ceiling Cooling & Ventilation",
                "allocation": alloc_fan,
                "items": [
                    {
                        "name": "Atomberg BLDC Energy Saving Fans",
                        "description": "Silent BLDC motor with smart remote control",
                        "estimated_price": int(alloc_fan / max(1, num_f)),
                        "quantity": num_f,
                        "search_terms": "atomberg bldc ceiling fan",
                        "shopping_links": {
                            "amazon": "https://www.amazon.in/s?k=atomberg+bldc+ceiling+fan",
                            "flipkart": "https://www.flipkart.com/search?q=atomberg+bldc+ceiling+fan",
                            "ikea": "https://www.ikea.com/in/en/search/?q=ceiling+fan"
                        }
                    }
                ]
            },
            {
                "category": "Living & Bedroom Furniture",
                "allocation": alloc_furn,
                "items": [
                    {
                        "name": "Contemporary Engineered Wood Table Set",
                        "description": "Modern minimalist interior design finish",
                        "estimated_price": int(alloc_furn / max(1, num_furn)),
                        "quantity": num_furn,
                        "search_terms": "modern living room table",
                        "shopping_links": {
                            "amazon": "https://www.amazon.in/s?k=modern+living+room+table",
                            "flipkart": "https://www.flipkart.com/search?q=modern+living+room+table",
                            "ikea": "https://www.ikea.com/in/en/search/?q=coffee+table"
                        }
                    }
                ]
            }
        ]
    }


# 2. PARTY & EVENT PLANNER ROUTE
@router.post("/party-budget")
def plan_party_budget(budget_input: PartyBudgetInput, request: Request):
    total_b = float(budget_input.total_budget or 25000)
    guests = int(budget_input.num_guests or 15)

    alloc_venue = int(total_b * 0.30)
    alloc_food = int(total_b * 0.50)
    alloc_decor = int(total_b - (alloc_venue + alloc_food))

    return {
        "total_budget": total_b,
        "remaining_budget": 0,
        "recommendation_type": "party",
        "timestamp": datetime.utcnow().isoformat(),
        "budget_breakdown": [
            {
                "category": "Venue & Space Booking",
                "allocation": alloc_venue,
                "items": [
                    {
                        "name": f"Private Event Space for {guests} Guests",
                        "description": "Air-conditioned celebration hall with seating",
                        "estimated_price": alloc_venue,
                        "quantity": 1,
                        "search_terms": "party hall venue",
                        "shopping_links": {
                            "swiggy": "https://www.swiggy.com/restaurants",
                            "zomato": "https://www.zomato.com",
                            "oyo": "https://www.oyorooms.com/search?location=banquet+hall"
                        }
                    }
                ]
            },
            {
                "category": "Catering & Refreshments",
                "allocation": alloc_food,
                "items": [
                    {
                        "name": "Deluxe Party Buffet & Drinks",
                        "description": "Multi-course starters, main dishes, desserts & beverages",
                        "estimated_price": alloc_food,
                        "quantity": 1,
                        "search_terms": "party catering buffet",
                        "shopping_links": {
                            "swiggy": "https://www.swiggy.com/search?query=party+catering",
                            "zomato": "https://www.zomato.com/search?q=catering",
                            "oyo": "https://www.oyorooms.com"
                        }
                    }
                ]
            },
            {
                "category": "Decorations & Ambience",
                "allocation": alloc_decor,
                "items": [
                    {
                        "name": "Themed Balloon & LED String Light Setup",
                        "description": "Photo backdrop, decorative lights, and party props",
                        "estimated_price": alloc_decor,
                        "quantity": 1,
                        "search_terms": "birthday party decoration kit",
                        "shopping_links": {
                            "swiggy": "https://www.swiggy.com/instamart",
                            "zomato": "https://www.zomato.com",
                            "oyo": "https://www.oyorooms.com"
                        }
                    }
                ]
            }
        ]
    }


# 3. JEWELRY PLANNER ROUTE
@router.post("/jewelry-budget")
def plan_jewelry_budget(
    total_budget: float = Form(...),
    occasion: str = Form(...),
    preferences: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    request: Request = None
):
    total_b = float(total_budget or 30000)
    image_path = None
    if image and image.filename:
        image_path = save_upload_file(image)

    alloc_primary = int(total_b * 0.60)
    alloc_secondary = int(total_b - alloc_primary)

    return {
        "total_budget": total_b,
        "remaining_budget": 0,
        "recommendation_type": "jewelry",
        "timestamp": datetime.utcnow().isoformat(),
        "jewelry_recommendations": [
            {
                "item_type": f"Signature {occasion.title()} Necklace Set",
                "description": f"Elegant craftsmanship curated for {occasion} with {preferences or 'traditional touch'}",
                "estimated_price": alloc_primary,
                "shopping_links": {
                    "amazon": "https://www.amazon.in/s?k=gold+plated+necklace+set",
                    "tanishq": "https://www.tanishq.co.in/shop/necklaces",
                    "myntra": "https://www.myntra.com/necklace-sets"
                }
            },
            {
                "item_type": "Complementary Earrings & Bangles Set",
                "description": "Matching classic studs/jhumkas with fine designer polish",
                "estimated_price": alloc_secondary,
                "shopping_links": {
                    "amazon": "https://www.amazon.in/s?k=designer+earrings+and+bangles",
                    "tanishq": "https://www.tanishq.co.in/shop/earrings",
                    "myntra": "https://www.myntra.com/earrings"
                }
            }
        ]
    }