# uvicorn fastapi_service:app --reload
from fastapi import FastAPI
import random
import json
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Load the cocktail data
with open('train_data.json', 'r') as file:
    train_data = json.load(file)
cocktail_data = train_data['cocktail_info']

# Load the flavor data
with open('flavor.json', 'r') as file:
    flavor_data = json.load(file)

# Create a dictionary for quick lookup of flavor profiles by ingredient name
flavor_dict = {item['name']: item for item in flavor_data}

class Preferences(BaseModel):
    flavor: str
    strength: str  # light, medium, strong
    glass_type: str
    include_ingredients: List[str]
    exclude_ingredients: List[str]
    alcoholic: bool

class CombinedFlavors(BaseModel):
    boozy: float
    sweet: float
    sour: float
    bitter: float
    umami: float
    salty: float
    astringent: float
    Perceived_temperature: float
    spicy: float
    herbal: float
    floral: float
    fruity: float
    nutty: float
    creamy: float
    smoky: float

class Cocktail(BaseModel):
    cocktail_name: str
    cocktail_glass: str
    category: str
    recipe: Dict[str, float]
    alcoholic: str
    combined_flavors: CombinedFlavors
    image_path: str

def calculate_combined_flavors(recipe: Dict[str, float], flavors: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    combined_flavors = {
        'boozy': 0.0, 'sweet': 0.0, 'sour': 0.0, 'bitter': 0.0,
        'umami': 0.0, 'salty': 0.0, 'astringent': 0.0, 'Perceived_temperature': 0.0,
        'spicy': 0.0, 'herbal': 0.0, 'floral': 0.0, 'fruity': 0.0, 'nutty': 0.0,
        'creamy': 0.0, 'smoky': 0.0
    }
    total_amount = sum(recipe.values())
    
    for ingredient, amount in recipe.items():
        if ingredient in flavors:
            flavor_profile = flavors[ingredient]
            for flavor, value in flavor_profile.items():
                if flavor not in ['name', 'ABV']:
                    combined_flavors[flavor] += value * (amount / total_amount)
    
    return combined_flavors

@app.post("/recommend", response_model=Cocktail)
def recommend_cocktail(preferences: Preferences):
    """
    Recommend a cocktail based on user preferences.
    """
    # Filter cocktails based on preferences
    filtered_cocktails = [cocktail for cocktail in cocktail_data if 
                          all(ingredient in cocktail['recipe'] for ingredient in preferences.include_ingredients) and
                          all(ingredient not in cocktail['recipe'] for ingredient in preferences.exclude_ingredients) and
                          (preferences.alcoholic == (cocktail['alcoholic'] == 'Alcoholic'))]

    # Select a random cocktail from the filtered list
    if filtered_cocktails:
        cocktail = random.choice(filtered_cocktails)
    else:
        cocktail = random.choice(cocktail_data)

    # Add flavor information
    flavors = {ingredient: flavor_dict[ingredient] for ingredient in cocktail['recipe'] if ingredient in flavor_dict}
    
    # Calculate combined flavors
    combined_flavors = calculate_combined_flavors(cocktail['recipe'], flavors)
    
    cocktail_response = {
        "cocktail_name": cocktail['cocktail_name'],
        "cocktail_glass": cocktail['cocktail_glass'],
        "category": cocktail['category'],
        "recipe": cocktail['recipe'],
        "alcoholic": cocktail['alcoholic'],
        "combined_flavors": combined_flavors,
        "image_path": f"./drinks_img/img_{random.randint(0, 41)}.jpg"  # Random image for now
    }

    return cocktail_response

@app.post("/flavors", response_model=CombinedFlavors)
def get_flavor_profile(preferences: Preferences):
    """
    Get the combined flavor profile based on the selected ingredients.
    """
    # Create a recipe dictionary with equal amounts for each ingredient
    recipe = {ingredient: 1.0 for ingredient in preferences.include_ingredients}
    
    # Add flavor information
    flavors = {ingredient: flavor_dict[ingredient] for ingredient in recipe if ingredient in flavor_dict}
    
    # Calculate combined flavors
    combined_flavors = calculate_combined_flavors(recipe, flavors)
    
    return combined_flavors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

