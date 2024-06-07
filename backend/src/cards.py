from collections import deque
from random import shuffle


class Card:
    SUITS = {
        1: "♣",
        2: "♦",
        3: "♥",
        4: "♠",
    }
    RANKS = {
        0: "🤡",
        1: "A",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "J",
        12: "Q",
        13: "K",
    }

    def __init__(self, rank: int, suit: int) -> None:
        if rank not in range(0, 14) or suit not in range(1, 5):
            raise ValueError("Invalid rank or suit")
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        rank_str = self.RANKS.get(self.rank, str(self.rank))
        suit_str = self.SUITS.get(self.suit, str(self.suit))
        return f"Card({rank_str}{suit_str})"

    def get_suit_char(self) -> str:
        """Returns suit character of card, (♣♦♥♠)

        Returns:
            str: suit of card as a single char string emoji
        """
        return self.SUITS[self.suit]

    def get_rank_char(self) -> str:
        """Returns rank character of card, A - K

        Returns:
            str: rank of card as a single char string,
                e.g. "K", "5", "J"
        """
        return self.RANKS[self.rank]

    def get_rank(self, aces_high: bool = False) -> int:
        """Returns rank of card, 1 - 13

        Args:
            aces_high (bool, optional): sets rank
                for A to 14 if true. Defaults to False.

        Returns:
            int: rank of card from 1 to 13,
            high ace is 14
        """
        rank = self.rank
        if rank == 1 and aces_high:
            rank = 14
        return rank

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank


class Deck(deque):
    def __init__(
        self, ranks=range(1, 14), suits=range(1, 5), repeats=1
    ) -> None:
        cards = [
            Card(rank, suit)
            for rank in ranks
            for suit in suits
            for _ in range(repeats)
        ]
        deque.__init__(self, cards)

    def shuffle(self) -> None:
        """Shuffle the Deck in place"""
        shuffle(self)

    def __repr__(self) -> str:
        return f"Deck({len(self)})"

    def __str__(self):
        return f"Card deck of size {len(self)})"

    def __iadd__(self, other):
        """Add cards from another deck to this deck

        Args:
            other (Deck): the deck to add cards from

        Returns:
            Deck: the updated deck
        """
        self.__add__(other)

    def __add__(self, other):
        """Add cards from another deck to a new deck

        Args:
            other (Deck): the deck to add cards from

        Returns:
            Deck: a new deck with the combined cards
        """
        if not isinstance(other, Deck):
            raise TypeError("Can only add Deck instances to a Deck")
        new_deck = Deck([])
        new_deck.extend(self)
        new_deck.extend(other)
        return new_deck
