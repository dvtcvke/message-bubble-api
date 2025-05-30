from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from .generate_bubbles import create_chat_image

app = FastAPI()

class ChatInput(BaseModel):
    text: str

@app.post("/generate")
def generate_image(input: ChatInput):
    output_path = create_chat_image(input.text)
    return FileResponse(output_path, media_type="image/jpeg")
