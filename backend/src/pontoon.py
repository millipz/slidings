from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pontoon_logic import Pontoon
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
games = {}

# Allow CORS for all origins (restrict this in a production environment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins, "*" means all
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods, "*" means all
    allow_headers=["*"],  # List of allowed headers, "*" means all
)

class GameID(BaseModel):
    game_id: str


@app.post("/start")
def start_game():
    game_id = str(uuid.uuid4())
    game = Pontoon()
    game.start_game()
    games[game_id] = game
    return {"game_id": game_id, "game_state": game.get_game_state()}


@app.post("/hit")
def hit(game_id: GameID):
    game = games.get(game_id.game_id)
    if not game:
        raise HTTPException(
            status_code=404, detail="Invalid game_id"
        )

    result = game.player_hit()
    return {"result": result, "game_state": game.get_game_state()}


@app.post("/stick")
def stick(game_id: GameID):
    game = games.get(game_id.game_id)
    if not game:
        raise HTTPException(
            status_code=404, detail="Invalid game_id"
        )
    result = game.player_stick()
    return {"result": result, "game_state": game.get_game_state()}


@app.get("/state")
def state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(
            status_code=404, detail="Invalid game_id"
        )

    return game.get_game_state()
