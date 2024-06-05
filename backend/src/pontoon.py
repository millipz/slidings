from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pontoon_logic import Pontoon
import uuid

app = FastAPI()
games = {}


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


@app.post("/stand")
def stand(game_id: GameID):
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
