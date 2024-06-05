import pytest
from src.cards import Card
from src.pontoon_logic import Pontoon

@pytest.fixture
def pontoon_game():
    return Pontoon()

def test_start_game(pontoon_game):
    pontoon_game.start_game()
    assert len(pontoon_game.player_hand) == 2
    assert len(pontoon_game.dealer_hand) == 2
    assert not pontoon_game.game_over
    assert not pontoon_game.player_stuck

def test_get_hand_value():
    pontoon_game = Pontoon()
    hand = [Card(1, 1), Card(10, 2), Card(5, 3)]  # Ace, 10, 5
    assert pontoon_game.get_hand_value(hand) == 16

    hand = [Card(1, 1), Card(1, 2), Card(10, 3)]  # Two Aces, 10
    assert pontoon_game.get_hand_value(hand) == 12  # Aces both 1s

    hand = [Card(1, 1), Card(1, 2), Card(1, 3), Card(10, 4)]  # Three Aces, 10
    assert pontoon_game.get_hand_value(hand) == 13  # All Aces 1

def test_hit(pontoon_game):
    pontoon_game.start_game()
    initial_player_hand_len = len(pontoon_game.player_hand)
    pontoon_game.hit(pontoon_game.player_hand)
    assert len(pontoon_game.player_hand) == initial_player_hand_len + 1

def test_is_busted(pontoon_game):
    hand = [Card(1, 1), Card(10, 2), Card(10, 3)]  # Ace, 10, 10
    assert not pontoon_game.is_busted(hand)

    hand = [Card(10, 1), Card(10, 2), Card(10, 3)]  # 10, 10, 10
    assert pontoon_game.is_busted(hand)

def test_player_hit(pontoon_game):
    pontoon_game.start_game()
    initial_player_hand_len = len(pontoon_game.player_hand)

    # Test successful hit
    result = pontoon_game.player_hit()
    status = result["status"]
    assert status == "success" or status == "busted"
    assert len(result["hand"]) == initial_player_hand_len + 1

def test_is_busted(pontoon_game):
    pontoon_game.start_game()

    # Test busted
    pontoon_game.player_hand = [Card(10, 1), Card(10, 2), Card(1, 3)]
    result = pontoon_game.get_game_state()
    assert result["player_value"] == 21
    result = pontoon_game.player_hit()
    assert result["status"] == "busted"
    assert pontoon_game.game_over

def test_error_on_hit_if_game_over(pontoon_game):
    pontoon_game.start_game()

    pontoon_game.game_over = True
    result = pontoon_game.player_hit()
    assert result["status"] == "error"

def test_error_on_hit_if_player_stuck(pontoon_game):
    pontoon_game.start_game()

    pontoon_game.game_over = False
    pontoon_game.player_stuck = True
    result = pontoon_game.player_hit()
    assert result["status"] == "error"

def test_player_stick(pontoon_game):
    pontoon_game.start_game()

    # Test player stick
    result = pontoon_game.player_stick()
    assert pontoon_game.player_stuck
    assert pontoon_game.game_over
    assert result["status"] in ["win", "loss", "tie"]

    # Test game already over
    pontoon_game.start_game()
    pontoon_game.game_over = True
    with pytest.raises(Exception):
        pontoon_game.player_stick()

def test_dealer_turn(pontoon_game):
    pontoon_game.start_game()
    pontoon_game.dealer_hand = [Card(5, 1), Card(6, 2)]  # 11
    pontoon_game.dealer_turn()
    assert pontoon_game.get_hand_value(pontoon_game.dealer_hand) >= 17

def test_check_winner(pontoon_game):
    pontoon_game.start_game()

    # Test player busted
    pontoon_game.player_hand = [Card(10, 1), Card(10, 2), Card(10, 3)]
    result = pontoon_game.check_winner()
    assert result["status"] == "loss"

    # Test dealer busted
    pontoon_game.player_hand = [Card(10, 1), Card(5, 2)]
    pontoon_game.dealer_hand = [Card(10, 1), Card(10, 2), Card(10, 3)]
    result = pontoon_game.check_winner()
    assert result["status"] == "win"

    # Test player wins
    pontoon_game.player_hand = [Card(10, 1), Card(10, 2)]
    pontoon_game.dealer_hand = [Card(5, 1), Card(6, 2)]
    result = pontoon_game.check_winner()
    assert result["status"] == "win"

    # Test dealer wins
    pontoon_game.player_hand = [Card(5, 1), Card(6, 2)]
    pontoon_game.dealer_hand = [Card(10, 1), Card(10, 2)]
    result = pontoon_game.check_winner()
    assert result["status"] == "loss"

    # Test tie
    pontoon_game.player_hand = [Card(10, 1), Card(10, 2)]
    pontoon_game.dealer_hand = [Card(10, 1), Card(10, 2)]
    result = pontoon_game.check_winner()
    assert result["status"] == "tie"

def test_get_game_state(pontoon_game):
    pontoon_game.start_game()

    # Test game not over
    game_state = pontoon_game.get_game_state()
    assert len(game_state["player_hand"]) == 2
    assert game_state["dealer_hand"] == [pontoon_game.dealer_hand[0], "Hidden"]
    assert game_state["player_value"] == pontoon_game.get_hand_value(pontoon_game.player_hand)
    assert game_state["dealer_value"] == "Hidden"
    assert not game_state["game_over"]
    assert not game_state["player_stuck"]

    # Test game over
    pontoon_game.game_over = True
    game_state = pontoon_game.get_game_state()
    assert len(game_state["dealer_hand"]) == 2
    assert game_state["dealer_value"] == pontoon_game.get_hand_value(pontoon_game.dealer_hand)
    assert game_state["game_over"]