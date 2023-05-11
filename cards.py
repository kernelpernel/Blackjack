"""
Set up a deck of cards to build a blackjack game.

Author: Ethan Purnell
Start: 4/30/23
"""

import random


class Card:
    """
    Creates the Card objects, which are used to build decks/shoes and play the game.
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            self.value = int(rank)
        elif rank in ['J', 'K', 'Q']:
            self.value = 10
        elif rank == 'A':
            self.value = 11

    def __str__(self):
        """
        String method for the class.
        :return: printed statement of what the card is.
        """
        return f'{self.rank} of {self.suit}'

    def showval(self):
        """
        Shows the value of the card.
        :return: no return, just prints the card value
        """
        print(f'{self.value}')


class Deck:
    """
    Class to construct a single deck from the set of cards.
    """
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Deck construction method called in the constructor. Iterates through all the cards and adds them to the deck.
        :return: no return, operates on the "cards" attribute of the deck.
        """
        for suit in ['Hearts', 'Clubs', 'Spades', 'Diamonds']:
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                self.cards.append(Card(suit, value))

    def show_all(self):
        """
        Prints every card in the deck.
        """
        for card in self.cards:
            print(card)

    def shuffle(self):
        """
        Shuffles the deck. Plan to replace with a coded shuffle algorithm.
        :return: no return, just rearranges the objects in the list.
        """
        random.shuffle(self.cards)

    def cards_remaining(self):
        """
        Prints the number of cards remaining in the deck.
        """
        print(f'There are {len(self.cards)} cards remaining in the deck.\n')

    def draw(self):
        """
        Draws a card from the deck.
        :return: a card object from the top of the deck.
        """
        return self.cards.pop()


class Shoe:
    """
    Class to build a blackjack "shoe" consisting of multiple decks.
    """
    def __init__(self, n_decks):
        self.cards = []
        self.size = n_decks
        self.build()

    def build(self):
        """
        Builds the shoe with a specified number of decks. Iterates over n_decks, creates a deck object, and adds those
        cards to the shoe.
        :return: no return, operates on the cards attribute
        """
        i = 1
        while i <= self.size:
            deck = Deck()
            self.cards.extend(deck.cards)
            i += 1

    def cards_remaining(self):
        """
        Prints a statement with the remaining number of cards.
        """
        print(f'There are {len(self.cards)} cards remaining in the shoe.')

    def shuffle(self):
        """
        Shuffles the deck. Would also like to replace this with a coded algorithm.
        :return:
        """
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


def main():
    deck = Shoe(3)
    deck.shuffle()
    deck.cards_remaining()
    for i in range(1, 11):
        card = deck.draw()
        print(card)
    deck.cards_remaining()


if __name__ == '__main__':
    main()
