from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to your needs
    allow_headers=["*"],  # Adjust this to your needs
)

# Mount the static directory to serve CSS and JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html at the root URL
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Define a simple rule-based response function
def get_bot_response(user_message: str) -> str:
    responses = [
        "Hello! How can I assist you today?",
        "I'm here to help. What do you need?",
        "Tell me more about your query.",
        "I'm not sure what you mean. Can you clarify?"
    ]
    return random.choice(responses)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: Message):
    user_message = message.message
    bot_reply = get_bot_response(user_message)
    return {"reply": bot_reply}
