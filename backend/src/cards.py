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
        if self.suit == other.suit and self.value == other.value:
            return True
        else:
            return False


class Deck:
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
        size=1
    ) -> None:
        self._cards = deque(
            [
                Card(value, suit)
                for value in values
                for suit in suits
                for _ in range(size)
            ]
        )

    def add_card(self, card: Card, to_bottom: bool = False):
        """Add a card to the deck

        Args:
            card (Card): card to add
            to_bottom (bool): add to bottom of deck
                defaults to False

        Returns:
            None
        """
        if not to_bottom:
            self._cards.append(card)
        else:
            self._cards.appendleft(card)
    
    def add_cards(self, cards: list[Card], to_bottom: bool = False):
        """Add list of cards to the deck

        Args:
            cards (list[Card]): cards to add
            to_bottom (bool): add to bottom of deck
                defaults to False

        Returns:
            None
        """
        if not to_bottom:
            self._cards.extend(cards)
        else:
            self._cards.extendleft(cards)
        return self

    def deal(self, from_bottom: bool = False) -> Card:
        """Deal a card from the top of the deck

        Args:
            from_bottom (bool): deal from bottom of deck
                defaults to False

        Returns:
            Card: the dealt card
            None: if empty
        """
        try:
            if not from_bottom:
                return self._cards.pop()
            else:
                return self._cards.popleft()
        except IndexError:
            return None
        
    def __iadd__(self, other):
        """Add card(s) to the deck using the += operator

        Args:
            other (Card or list[Card]): card(s) to add

        Returns:
            Deck: the updated deck
        """
        if isinstance(other, Card):
            self._cards.append(other)
        else:
            self._cards.extend(other)
        return self

    def __len__(self):
        return len(self._cards)

    def __repr__(self) -> str:
        return f"Deck({len(self)})"

    def __str__(self):
        return f'Card deck of size {len(self)})'

    def __getitem__(self, index):
        return self._cards[index]

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        else:
            for i in range(0, len(self)):
                if self._cards[i] != other[i]:
                    return False
            return True
