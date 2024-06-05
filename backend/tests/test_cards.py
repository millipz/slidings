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
        assert one_card_deck.pop() == Card("A", "♦")
        assert len(one_card_deck) == 0

    def test_empty_deck_raises_index_error_on_deal(slef):
        one_card_deck = Deck(["A"], ["♦"])
        one_card_deck.pop()
        assert len(one_card_deck) == 0
        with pytest.raises(IndexError):
            one_card_deck.pop()

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
        test_deck.append(card_to_add)
        assert len(test_deck) == 53
        assert test_deck.pop() == Card("4", "♣")

    def test_adding_and_dealing_from_top_and_bottom(self):
        test_deck = Deck(["5"], ["♦"])
        assert len(test_deck) == 1
        test_deck.append(Card("4", "♣"))
        assert len(test_deck) == 2
        test_deck.appendleft(Card("2", "♥"))
        assert len(test_deck) == 3
        assert test_deck.pop() == Card("4", "♣")
        assert test_deck.popleft() == Card("2", "♥")

    def test_adding_multiple_card_objects_using_extend_method(self):
        cards = [Card(v, s) for v, s in [("4", "♣"), ("2", "♥"), ("5", "♦")]]
        three_cards = Deck([])
        three_cards.extend(cards)
        assert len(three_cards) == 3

    def test_deck_iteration(self):
        cards = [Card(v, s) for v, s in [("4", "♣"), ("2", "♥"), ("5", "♦")]]
        print(cards)
        three_cards = Deck([])
        three_cards.extend(cards)
        iterator = iter(three_cards)
        assert next(iterator) == Card("4", "♣")
        assert next(iterator) == Card("2", "♥")
        assert next(iterator) == Card("5", "♦")
        with pytest.raises(StopIteration):
            next(iterator)

    def test_adding_decks(self):
        four_of_clubs = Deck([])
        four_of_clubs.append(Card("4", "♣"))
        two_of_hearts = Deck([])
        two_of_hearts.append(Card("2", "♥"))
        two_cards = four_of_clubs + two_of_hearts
        assert len(two_cards) == 2
        assert all(
                [
                    card in two_cards for card in [
                        Card("4", "♣"),
                        Card("2", "♥"),
                    ]
                ]
            )
