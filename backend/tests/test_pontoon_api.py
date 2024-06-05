from fastapi.testclient import TestClient
from src.pontoon import app, games

client = TestClient(app)

def test_start_game():
    response = client.post("/start")
    assert response.status_code == 200
    data = response.json()
    assert "game_id" in data
    assert "game_state" in data

    game_id = data["game_id"]
    game_state = data["game_state"]
    assert len(game_state["player_hand"]) == 2
    assert len(game_state["dealer_hand"]) == 2
    assert not game_state["game_over"]

    assert game_id in games

def test_hit():
    # Start a new game
    start_response = client.post("/start")
    game_id = start_response.json()["game_id"]

    # Test hitting
    hit_response = client.post("/hit", json={"game_id": game_id})
    assert hit_response.status_code == 200
    data = hit_response.json()
    assert "result" in data
    assert "game_state" in data
    hand = data["game_state"]["player_hand"]
    value = data["game_state"]["player_value"]
    game_over = data["game_state"]["game_over"]
    assert len(hand) == 3
    if value <= 21:
        assert not game_over
    else:
        assert game_over


def test_stand():
    # Start a new game
    start_response = client.post("/start")
    game_id = start_response.json()["game_id"]

    # Test standing
    stand_response = client.post("/stand", json={"game_id": game_id})
    assert stand_response.status_code == 200
    data = stand_response.json()
    assert "result" in data
    assert "game_state" in data

    game_state = data["game_state"]
    assert game_state["game_over"] == True

def test_state():
    # Start a new game
    start_response = client.post("/start")
    game_id = start_response.json()["game_id"]

    # Test getting the game state
    state_response = client.get(f"/state?game_id={game_id}")
    assert state_response.status_code == 200
    data = state_response.json()
    assert "player_hand" in data
    assert "dealer_hand" in data
    assert "game_over" in data

def test_invalid_game_id():
    # Test with an invalid game_id
    invalid_game_id = "invalid_id"
    hit_response = client.post("/hit", json={"game_id": invalid_game_id})
    assert hit_response.status_code == 404
    assert hit_response.json()["detail"] == "Invalid game_id"

    stand_response = client.post("/stand", json={"game_id": invalid_game_id})
    assert stand_response.status_code == 404
    assert stand_response.json()["detail"] == "Invalid game_id"

    state_response = client.get(f"/state?game_id={invalid_game_id}")
    assert state_response.status_code == 404
    assert state_response.json()["detail"] == "Invalid game_id"