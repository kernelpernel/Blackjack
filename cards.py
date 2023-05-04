"""
Set up a deck of cards to build a blackjack game.

Author: Ethan Purnell
Start: 4/30/23
"""

import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            self.value = int(rank)
        elif rank in ['J', 'K', 'Q']:
            self.value = 10
        elif rank == 'A':                                    #Ace should be 1 or 11? Implement option to have 1 or 11
            self.value = 11

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    def showval(self):
        print(f'{self.value}')


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ['Hearts', 'Clubs', 'Spades', 'Diamonds']:
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                self.cards.append(Card(suit, value))

    def show_all(self):
        for card in self.cards:
            card.showfull()

    def shuffle(self):
        random.shuffle(self.cards)

    def cards_remaining(self):
        print(f'There are {len(self.cards)} cards remaining in the deck.\n')

    def draw(self):
        return self.cards.pop()


class Shoe:
    def __init__(self, n_decks):
        self.cards = []
        self.size = n_decks
        self.build()

    def build(self):
        i = 1
        while i <= self.size:
            deck = Deck()
            self.cards.extend(deck.cards)
            i += 1

    def cards_remaining(self):
        print(f'There are {len(self.cards)} cards remaining in the shoe.')

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


def main():
    deck = Deck()
    deck.shuffle()

    card = deck.draw()
    print(card)

    card.showval()


if __name__ == '__main__':
    main()
