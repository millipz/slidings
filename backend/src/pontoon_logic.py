from src.cards import Deck


class GameOverException(Exception):
    pass


class Pontoon:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.player_stuck = False

    def start_game(self):
        self.deck = Deck()  # Fresh deck
        self.deck.shuffle()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.game_over = False
        self.player_stuck = False

    def get_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card.get_rank()
            if rank == 1:  # Ace
                aces += 1
                value += 11
            elif rank > 10:  # Face cards
                value += 10
            else:
                value += rank
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def hit(self, hand):
        hand.append(self.deck.pop())
        return hand

    def is_busted(self, hand):
        return self.get_hand_value(hand) > 21

    def player_hit(self):
        if self.player_stuck or self.game_over:
            return {
                "status": "error",
                "message": "Game over or player has already stood.",
            }

        self.hit(self.player_hand)
        if self.is_busted(self.player_hand):
            self.game_over = True
            return {
                "status": "busted",
                "message": "Player busted!",
                "hand": self.player_hand,
            }
        return {"status": "success", "hand": self.player_hand}

    def player_stick(self):
        if self.game_over:
            raise GameOverException("The game is over")
        self.player_stuck = True
        self.dealer_turn()
        self.game_over = True
        return self.check_winner()

    def dealer_turn(self):
        while self.get_hand_value(self.dealer_hand) < 17:
            self.hit(self.dealer_hand)
        if self.is_busted(self.dealer_hand):
            self.game_over = True

    def check_winner(self):
        player_value = self.get_hand_value(self.player_hand)
        dealer_value = self.get_hand_value(self.dealer_hand)

        result = {
            "player_hand": self.player_hand,
            "dealer_hand": self.dealer_hand,
            "player_value": player_value,
            "dealer_value": dealer_value,
        }

        if player_value > 21:
            result.update(
                {"status": "loss", "message": "Dealer wins!"}
            )
        elif dealer_value > 21 or player_value > dealer_value:
            result.update(
                {"status": "win", "message": "Player wins!"}
            )
        elif player_value < dealer_value:
            result.update(
                {"status": "loss", "message": "Dealer wins!"}
            )
        else:
            result.update(
                {"status": "tie", "message": "It's a tie!"}
            )

        return result

    def get_game_state(self):
        return {
            "player_hand": self.player_hand,
            "dealer_hand": (
                self.dealer_hand
                if self.game_over
                else [self.dealer_hand[0], "Hidden"]
            ),
            "player_value": self.get_hand_value(self.player_hand),
            "dealer_value": (
                self.get_hand_value(self.dealer_hand)
                if self.game_over
                else "Hidden"
            ),
            "game_over": self.game_over,
            "player_stuck": self.player_stuck,
        }
