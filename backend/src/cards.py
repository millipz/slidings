from collections import deque

SUITS: list[str] = tuple(
    "♣ ♦ ♥ ♠".split()
    )
VALUES: list[str] = tuple(
    "A 2 3 4 5 6 7 8 9 10 J Q K".split()
    )
VALID_SUITS: list[str] = tuple(
    "♣ ♦ ♥ ♠ 🤡".split()
    )
VALID_VALUES: list[str] = tuple(
    "A 2 3 4 5 6 7 8 9 10 J Q K 🤡".split()
    )


class Card:
    """
    A basic playing card class

    ...

    Attributes
    ----------
    value : str
        a character representing the value from A-K
    suit : str
        an emoji/symbol of the suit [♣ ♦ ♥ ♠]
    rank : int


    Methods
    -------
    get_rank(aces_high = False)
        Returns an integer representing the rank
        A = 1, K = 13. A = 14 if aces_high.
    """
    def __init__(self, value: str, suit: str) -> None:
        if (
            value not in VALID_VALUES
            or suit not in VALID_SUITS
        ):
            raise KeyError
        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f"Card({self.value}{self.suit})"

    def get_rank(self, aces_high: bool = False) -> int:
        """Returns rank of card, 0 - 14

        Args:
            aces_high (bool, optional): sets rank
                for A to 14 if true. Defaults to False.

        Returns:
            int: rank of card from 0 to 14,
            joker is 0, high ace is 14
        """
        try:
            return int(self.value)
        except ValueError:
            match self.value:
                case "🤡":
                    return 0
                case "J":
                    return 11
                case "Q":
                    return 12
                case "K":
                    return 13
                case "A":
                    return 14 if aces_high else 1
                
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value


class Deck(deque):
    """
    A basic playing card deck class
    (can also be used as a hand)

    ...

    Attributes
    ----------
    ranks : list[int]
        a list of the ranks in the deck
        A - K
    suits : list[str]
        a list of the suits in the deck
        defaults to ["♣", "♦", "♥", "♠"]

    Methods
    -------
    get_rank(aces_high = False)
        Returns an integer representing the rank
        A = 1, K = 13. A = 14 if aces_high.
    """
    def __init__(
        self,
        values: list[str] = VALUES,
        suits: list[str] = SUITS,
        repeats=1
    ) -> None:
        return deque.__init__(
            self,
            [
                Card(value, suit)
                for value in values
                for suit in suits
                for _ in range(repeats)
            ],
        )

    def __repr__(self) -> str:
        return f"Deck({len(self)})"

    def __str__(self):
        return f'Card deck of size {len(self)})'

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
        self.extend(other)
        return self
