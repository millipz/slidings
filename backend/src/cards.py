from collections import deque

SUITS: list[str] = tuple("♣ ♦ ♥ ♠".split())
VALUES: list[str] = "A 2 3 4 5 6 7 8 9 10 J Q K".split()


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
        if value not in VALUES or suit not in SUITS:
            raise KeyError
        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f"Card({self.value}{self.suit})"

    def get_rank(self, aces_high: bool = False):
        try:
            return int(self.value)
        except ValueError:
            match self.value:
                case "J":
                    return 11
                case "Q":
                    return 12
                case "K":
                    return 13
                case "A":
                    return 14 if aces_high else 1


class Deck:
    def __init__(
        self, suits: list[str] = SUITS, values: list[str] = VALUES, size=1
    ) -> None:
        self.cards = deque(
            [
                Card(value, suit)
                for value in values
                for suit in suits
                for _ in range(size)
            ]
        )
