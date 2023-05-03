"""
Control class for the blackjack game.

Author: Ethan Purnell
Date: 4/30/23
"""
import people
import time
from cards import Shoe
from cards import Deck
import math
import random


class Blackjack:
    def __init__(self):
        self.bettors = []
        self.dealer = people.Dealer()
        self.shoe = []
        self.stop = 0
        self.n_decks = 0
        self.minimum_bet = 0
        self.player_bets = {}

    def initialize_game(self):
        n_decks = input('\nHow many decks would you like to have in the shoe? ')
        try:
            if int(n_decks) < 0:
                print('\nThere has to be a positive number of decks. Please try again.')
                self.initialize_game()
            elif int(n_decks) > 12:
                print('\nThat\'s a lot of decks. Let\'s keep it under 12. Please try again.')
                self.initialize_game()
            else:
                self.n_decks = int(n_decks)

        except ValueError:
            print('\nThat was an invalid input. Please try again. ')
            self.initialize_game()

        self.shoe = self.initialize_deck()
        self.shoe.shuffle()
        self.shoe.shuffle()
        self.initialize_players()
        self.stop = self.set_stop()
        self.minimum_bet = self.set_min_bet()

    def initialize_players(self):
        participants = {}
        print('\nWe\'re glad to see you here! Please follow the prompts to identify the players.')

        add = True
        while add:
            name = input('\nPlease enter your name: ')
            # TODO: Make robust against bad input
            capital = int(input('\nPlease enter the amount of money you are playing with: '))
            participant = {name: capital}
            participants.update(participant)

            more = input('\nIs there anyone else playing? (Y/N) ')
            if more.upper() == 'Y':
                pass
            elif more.upper() == 'N':
                add = False
            else:
                print('\nYou did not enter a valid input. Please initialize the game again...')

        for key, value in participants.items():
            self.bettors.append(people.Bettor(name=key, money=value))

    def set_min_bet(self):
        min_bet = input('\nPlease enter the minimum bet for the table: ')
        try:
            if int(min_bet) > 0:
                return int(min_bet)
            else:
                print('\nThe minimum bet must be a positive number or zero. Please try again. ')
                self.set_min_bet()

        except ValueError:
            print('\nThat was not a valid input. Please enter a positive number or zero: ')
            self.set_min_bet()

    def initialize_deck(self):
        if self.n_decks == 1:
            return Deck()
        else:
            return Shoe(self.n_decks)

    def set_stop(self):
        low = math.floor(0.25 * len(self.shoe.cards))
        high = math.floor(0.5 * len(self.shoe.cards))

        return random.randint(low, high)

    def deal(self):
        print(f'\nThere are {len(self.shoe.cards)} cards remaining.')

        if len(self.shoe.cards) < self.stop:
            print('\nReshuffling deck...')
            self.shoe = self.initialize_deck()
            self.stop = self.set_stop()
            self.shoe.shuffle()
            self.shoe.shuffle()

        for i in range(2):
            for bettor in self.bettors:
                card = self.shoe.draw()
                bettor.hand.append(card)

            card = self.shoe.draw()
            self.dealer.hand.append(card)

    def bet(self):
        for bettor in self.bettors:
            print(f'\n{bettor.name} is betting...')
            good_bet = False
            while not good_bet:
                bet = bettor.place_bet()
                if bet < self.minimum_bet:
                    print(f'\nYour bet was below the minimum bet of {self.minimum_bet}. Please try again. ')
                    bettor.bankroll += bet
                else:
                    self.player_bets.update({bettor.name: bet})
                    good_bet = True

    def hit(self, player):
        card = self.shoe.draw()
        player.hand.append(card)
        if isinstance(player, people.Dealer):
            player.show_hand(showall=True)

        else:
            player.show_hand()
            print(f'\n{player.name}\'s score is: {player.calculate_score}')

    def player_choice(self):
        choice = input('\nPlease enter the number corresponding to what you would like to do: '
                       '\n   1) Hit. '
                       '\n   2) Stand. '
                       '\n   3) Double down.\n')

        if choice not in ['1', '2', '3']:
            print('\nYou provided an invalid input. Please try again. ')
            self.player_choice()
        else:
            return int(choice)

    def pay_winners(self):
        for bettor in self.bettors:
            if not bettor.is_busted:
                print(f'\n{bettor.name} wins {self.player_bets[bettor.name]}!')
                bettor.bankroll += 2 * self.player_bets[bettor.name]

    def compare_hands(self, player):
        if player.is_busted:
            print(f'\n{player.name} was busted.')
        elif player.calculate_score > self.dealer.calculate_score:
            print(f'\n{player.name} wins! ')
            player.bankroll += self.player_bets[player.name] * 2
        elif player.calculate_score == self.dealer.calculate_score:
            print(f'\n{player.name} had a draw. ')
            player.bankroll += self.player_bets[player.name]
        elif player.calculate_score < self.dealer.calculate_score:
            print(f'\n{player.name} loses... ')

    def player_reset(self):
        for bettor in self.bettors:
            bettor.reset()

        self.dealer.reset()

    def play_again(self):
        ask = True
        while ask:
            choice = input('\nWould you like to play again? (Y/N) ')

            if choice.upper() == 'Y':
                return True
            elif choice.upper() == 'N':
                return False
            else:
                print('\nYou did not provide a valid input. Please try again. ')

    def play(self):
        print('+----------------Welcome to the casino!----------------+')
        self.initialize_game()
        running = True
        while running:
            self.bet()
            self.deal()
            for bettor in self.bettors:
                print(f'\n{bettor.name} is playing... ')
                next_player = False
                self.dealer.show_hand()
                bettor.show_hand()
                print(f'\n{bettor.name} has {bettor.calculate_score}')
                while not next_player:
                    choice = self.player_choice() # TODO: don't make choice if player gets blackjack, and adjust payout

                    if choice == 1:
                        print(f'{bettor.name} hits...')
                        time.sleep(1)
                        self.hit(bettor)

                    elif choice == 2:
                        bettor.stand()
                        next_player = True

                    elif choice == 3: # TODO: implement controls to make sure the player can only do this once
                        bettor.bankroll -= self.player_bets[bettor.name]
                        self.player_bets[bettor.name] = self.player_bets[bettor.name] * 2
                        self.hit(bettor)
                        next_player = True

                    if bettor.is_busted:
                        bettor.bust()
                        next_player = True

            dealers_turn = True
            self.dealer.show_hand(True)
            while dealers_turn:
                if self.dealer.calculate_score < 17:
                    print('\nDealer hits... ')
                    time.sleep(1)
                    self.hit(self.dealer)
                    time.sleep(2)

                if self.dealer.calculate_score >= 17 and not self.dealer.is_busted:
                    self.dealer.stand()
                    break

                if self.dealer.is_busted:
                    self.dealer.bust()
                    self.pay_winners()
                    break

            if not self.dealer.is_busted:
                for bettor in self.bettors:
                    self.compare_hands(bettor)

            again = self.play_again()
            if not again:
                print('\nThanks for playing! See you next time. ')
                running = False

            self.player_reset()


def main():
    # TODO: monitor time spent playing, give gambling hotline info after threshold
    # TODO: add split
    # TODO: handle blackjack properly
    # TODO: make choice menu dynamic based on what is available to the player (i.e. no split if card values not the
    # TODO:     same, no double down if you hit)
    # TODO: kick player out of table if their bankroll drops below the minimum bet (or give them the chance to go to the ATM)

    game = Blackjack()
    game.play()


if __name__ == '__main__':
    main()



