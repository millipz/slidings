from src.cards import Card
import pytest


class TestCardClass:
    def test_invalid_values_raise_key_error(self):
        with pytest.raises(KeyError):
            _ = Card("1", "1")
        with pytest.raises(KeyError):
            _ = Card("2", "spades")

    def test_card_created_with_suit_and_value(self):
        ace_of_spades = Card("A", "♠")
        assert (
            ace_of_spades.suit == "♠" and
            ace_of_spades.value == "A"
        )

    def test_integer_rank_available(self):
        four_of_hearts = Card("4", "♥")
        ace_of_diamonds = Card("A", "♦")
        king_of_clubs = Card("K", "♣")
        assert (
            four_of_hearts.get_rank() == 4 and
            ace_of_diamonds.get_rank() == 1 and
            king_of_clubs.get_rank() == 13
        )

    def test_integer_rank_returns_14_for_aces_high(self):
        ace_of_diamonds = Card("A", "♦")
        assert (
            ace_of_diamonds.get_rank(aces_high=True) == 14
        )
