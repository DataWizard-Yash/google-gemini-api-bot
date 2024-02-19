from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class InputText(BaseModel):
    text: str

class OutputText(BaseModel):
    generated_text: str

@app.post("/bot", response_model=OutputText)
async def generate_story(payload: InputText):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyAK1vDq6hoOv6pFCLkMIUFYJsVquOLEu8Y"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": payload.text}]}]}, headers=headers)
        response.raise_for_status()
        # Extract the generated text content from the response JSON
        generated_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return {"generated_text": generated_text}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
