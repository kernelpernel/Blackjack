"""
Class definitions for players in a blackjack game.

Author: Ethan Purnell
Start Date: 4/30/23
"""

from cards import Shoe

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name

    def show_hand(self):
        print(f'\n{self.name} has: {[str(card) for card in self.hand]}')

    def reset(self):
        self.hand = []

    def stand(self):
        print(f'\n{self.name} stands on {self.calculate_score}.')

    def bust(self):
        print(f'\n{self.name} busts with score of {self.calculate_score}.')

    def blackjack(self):
        print(f'\n{self.name} has blackjack!')

    @property
    def calculate_score(self):
        score = 0

        ace = False
        for card in self.hand:
            score += card.value

            if card.rank == 'A':
                ace = True

            if score > 21 and ace:
                score -= 10
                ace = False

        return score

    @property
    def is_busted(self):
        return self.calculate_score > 21


class Dealer(Player):
    def __init__(self):
        super().__init__(name='Dealer')

    def show_hand(self, showall=False):
        if not showall:
            print(f'\nDealer showing: {self.hand[0]}, ???')

        else:
            print(f'\nDealer has: {[str(card) for card in self.hand]}')


class Bettor(Player):
    def __init__(self, name, money):
        super().__init__(self)
        self.bankroll = money
        self.name = name

    def place_bet(self):
        bet = input(f'\nYour bankroll is {self.bankroll} dollars. How much would you like to bet? ')

        try:
            if int(bet) > self.bankroll:
                print('\nYou do not have that much money. Please try again.')
                self.place_bet()

            else:
                self.bankroll -= int(bet)
                return int(bet)

        except ValueError:
            print('\nThat is not a valid bet entry. Please enter a number less than your bankroll.')
            self.place_bet()


def main():
    ethan = Bettor(name='Ethan', money=1000)
    print(ethan.calculate_score)
    shoe = Shoe(3)
    shoe.shuffle()

    ethan.hand.append(shoe.draw())
    ethan.hand.append(shoe.draw())
    ethan.show_hand()
    print(ethan.calculate_score)

    print(ethan.bankroll)

    ethan.place_bet()

    print(ethan.bankroll)


if __name__ == '__main__':
    main()