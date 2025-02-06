from fastapi import FastAPI
from pydantic import BaseModel
from llm_handler import generate_character_response
from data_loader import load_character_data

app = FastAPI()

# 🧠 Memory storage: Store user context
## TODO DUS DIE SHITTER VALT DE HELE TIJD IN HERHALING EN ONTHOUD DIE DING NIET
session_data = {}

class Query(BaseModel):
    session_id: str
    anime: str
    character: str
    wattpad_url: str
    message: str

@app.post("/chat")
def chat(query: Query):
    session_id = query.session_id
    anime = query.anime
    character = query.character
    wattpad_url = query.wattpad_url
    user_message = query.message

    # 🟢 Check if it's a new session
    if session_id not in session_data:
        load_character_data(anime, character)  # Scrape character data once
        session_data[session_id] = {
            "character": character,
            "messages": []  # Store full conversation history
        }

    # 📝 Store user message in session
    session_data[session_id]["messages"].append(user_message)

    # 🔄 Generate AI response using full conversation history
    conversation_history = "\n".join(session_data[session_id]["messages"])
    response = generate_character_response(conversation_history, character, anime)

    # 📝 Store AI response for memory
    session_data[session_id]["messages"].append(response)
    print(session_data[session_id]["messages"])

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
