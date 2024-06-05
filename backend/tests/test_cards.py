from src.cards import Card, Deck, SUITS, VALUES
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
  
    def test_alike_cards_are_equal(self):
        assert Card("A", "♦") == Card("A", "♦")


class TestDeck:
    def test_single_card_deck_has_length_1(self):
        one_card_deck = Deck(["A"], ["♦"])
        assert len(one_card_deck) == 1

    def test_single_card_deck_deal_method_returns_card(self):
        one_card_deck = Deck(["A"], ["♦"])
        assert one_card_deck.deal() == Card("A", "♦")
        assert len(one_card_deck) == 0

    def test_empty_deck_returns_none_on_deal(slef):
        one_card_deck = Deck(["A"], ["♦"])
        one_card_deck.deal()
        assert len(one_card_deck) == 0
        assert one_card_deck.deal() is None

    def test_default_creation_of_52_card_deck(self):
        full_deck = Deck()
        assert len(full_deck) == 52

    def test_all_cards_in_default_52_card_deck(self):
        full_deck = Deck()
        card_list = [
            (card.value, card.suit)
            for card in full_deck
            ]
        assert all([
            (v, s) in card_list
            for v in VALUES
            for s in SUITS
            ])
    
    def test_adding_to_top_of_deck(self):
        test_deck = Deck()
        card_to_add = Card("4", "♣")
        test_deck.add(card_to_add)
        assert len(test_deck) == 53
        assert test_deck.deal() == Card("4", "♣")

    def test_adding_and_dealing_from_top_and_bottom(self):
        test_deck = Deck(["5"], ["♦"])
        assert len(test_deck) == 1
        test_deck.add(Card("4", "♣"))
        assert len(test_deck) == 2
        test_deck.add(Card("2", "♥"), to_bottom=True)
        assert len(test_deck) == 3
        assert test_deck.deal() == Card("4", "♣")
        assert test_deck.deal(from_bottom=True) == Card("2", "♥")