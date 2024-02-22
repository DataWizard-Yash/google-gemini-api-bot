from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import markdown
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key="AIzaSyAK1vDq6hoOv6pFCLkMIUFYJsVquOLEu8Y")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings
)

class InputText(BaseModel):
    text: str

class OutputText(BaseModel):
    generated_text: str

@app.post("/bot", response_model=OutputText)
async def generate_story(payload: InputText):
    try:
        response = model.continue_chat(payload.text)
        return {"generated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/", response_model=OutputText)
async def chat_with_model(payload: InputText):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyAK1vDq6hoOv6pFCLkMIUFYJsVquOLEu8Y"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": payload.text}]}]}, headers=headers)
        response.raise_for_status()
        # Extract the generated text content from the response JSON
        generated_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        formatted_response = markdown.markdown(generated_text)
        return {"generated_text": formatted_response}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
