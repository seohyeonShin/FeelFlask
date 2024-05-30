from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import json
from CocktailEmbeddingMaker import Eval
from typing import List, Dict

app = FastAPI()

# Load your trained LSTM model
model = tf.keras.models.load_model('testmodel.h5')

with open('./train_data.json', 'r') as f:
    json_data = json.load(f)

with open('./flavor.json', 'r') as f:
    flavor_data = json.load(f)


class Features(BaseModel):
    ABV: float
    sweet: float
    sour: float
    bitter: float
    spicy: float
    herbal: float
    floral: float
    fruity: float
    nutty: float
    boozy: float
    astringent: float
    umami: float
    salty: float
    perceived_t: float
    creamy: float
    smoky: float

class Recipe(BaseModel):
    recipe: Dict[str, float]
    profile: Dict[str, float]



@app.post("/predict", response_model=Recipe)
async def predict(features: Features):
    # Extract input features

    # Predict using the model
    try:

        input_features = {'ABV': features.ABV,
                          'sweet' : features.sweet,
                          'sour' : features.sour,
                          'bitter' : features.bitter,
                          'spicy' : features.spicy,
                          'herbal' : features.herbal,
                          'floral' : features.floral,
                          'fruity' : features.fruity,
                          'nutty' : features.nutty,
                          'boozy' : features.boozy,
                          'astringent' : features.astringent,
                          'umami' : features.umami,
                          'salty' : features.salty,
                          'Perceived_temperature' : features.perceived_t,
                          'creamy' : features.creamy,
                          'smoky' : features.smoky
                          }

        eval_obj = Eval(json_data, flavor_data, model)

        # !seed ingredient는 나중에 구현하도록 함.! -> triple sec에서 입력받은 ingredient값으로 대체
        recipe_length = 5
        generated_recipes = eval_obj.generate_recipe('triple sec', input_features, recipe_length)
        result_recipe = {}

        total_amount = 200 # 200ml로 가정

        for recipe, ingredients in zip(generated_recipes[0], generated_recipes[1]):
            result_recipe[recipe]=ingredients * total_amount

        user_recipe_profile = eval_obj.get_taste_log(generated_recipes)

        return {"recipe" : result_recipe,
                "profile" : user_recipe_profile}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
