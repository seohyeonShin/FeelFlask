from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

app = FastAPI()

# Load your trained LSTM model
model = tf.keras.models.load_model('path_to_your_model.h5')

class Features(BaseModel):
    ABV: float
    boozy: float
    sweet: float
    sour: float
    bitter: float
    umami: float
    salty: float
    astringent: float
    perceived_t: float
    spicy: float
    herbal: float
    floral: float
    fruity: float
    nutty: float
    creamy: float
    smoky: float

@app.post("/predict/")
async def predict(features: Features):
    # Extract input features
    input_features = np.array([
        features.ABV,
        features.boozy,
        features.sweet,
        features.sour,
        features.bitter,
        features.umami,
        features.salty,
        features.astringent,
        features.perceived_t,
        features.spicy,
        features.herbal,
        features.floral,
        features.fruity,
        features.nutty,
        features.creamy,
        features.smoky
    ]).reshape(1, -1)

    # Predict using the model
    try:
        # Assuming the model outputs a recipe in the desired format
        prediction = model.predict(input_features)
        recipe = {f"{i}": amount for i, amount in enumerate(prediction[0])}
        return {"recipe": recipe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
