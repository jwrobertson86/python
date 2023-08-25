'''
Blackjack game class file.
'''

import random
import bj_errors

class Card():
    '''
    Describes a playing card.
    '''
    def __init__(self, suit, rank):
        '''
        Constructor for Card.
        '''
        self.suit = suit
        self.rank = rank
        

    def __str__(self):
        '''
        Define text output for Card.
        '''
        return self.rank[0] + self.suit


class Deck():
    '''
    Describes a deck of playing cards
    '''
    def __init__(self):
        '''
        Constructor for Deck.
        Creates 52 cards and shuffles them.
        '''
        suits = ['♠', '♦', '♥', '♣']
        ranks = [('A', 11), ('2', 2),  ('3', 3), ('4', 4), ('5', 5), 
                 ('6', 6),  ('7', 7),  ('8', 8), ('9', 9), ('10', 10),
                 ('J', 10), ('Q', 10), ('K', 10)]
        
        random.shuffle(suits)
        random.shuffle(ranks)
                 
        cards = []

        for s in suits:
            for r in ranks:
                cards.append(Card(s, r))

        random.shuffle(cards)

        self.cards = cards


    def __str__(self):
        '''
        Define text output for Deck. Mostly useful for debug purposes.
        '''
        output = []

        for c in self.cards:
            output.append(str(c))
            
        return ', '.join(output)


    def deal_card(self):
        '''
        Returns one card, popped off the top. (We don't want a shifty dealer dealing 
        off the bottom like in the Maverick movie.)
        '''

        return self.cards.pop(0)


# It occurs to me that the Dealer can probably also be of Player() class, and just
# ignore the payroll bit, and operate according to different logic in the game area.
# Course solution was to just create a Hand object instead, but they had no recurring
# chip total.
class Player():
    '''
    Describes a blackjack player.
    '''
    def __init__(self):
        '''
        Constructor for Player. Gives them a starting bankroll and a card list.
        '''
        self.bankroll = 100
        self.cards = []
        self.hand_val = 0


    def __str__(self):
        '''
        Define text output for Player.
        '''
        output = []

        for c in self.cards:
            output.append(str(c))
            
        return ', '.join(output) + " ({})".format(self.hand_val)


    def bet(self, amount):
        '''
        Places a bet. If the player has the amount, it deducts that amount from
        the player's bankroll. If not, it throws an exception and exits without
        doing anything.
        '''
        # Check the amount.
        if amount <= self.bankroll:
            self.bankroll -= amount
        else:   # If it's too big, throw the exception. It'll be handled in the game code.
            raise bj_errors.BetTooLarge


    def payout(self, amount):
        '''
        Receives the payout and deposits it into the player's bankroll.
        '''
        self.bankroll += amount


    def get_hand_val(self):
        '''
        Calculate hand value. Will account for the existence of Aces.
        '''
        val = 0
        hasAce = False

        for c in self.cards:
            val += c.rank[1] # Add number

            if not hasAce: # If an Ace hasn't already been flagged...
                hasAce = (c.rank[0] == 'A') # Test for an Ace.

        if val > 21 and hasAce: # If we're over 21 but we have an Ace...
            val -= 10           # Get rid of one Ace's worth of abiguity.

        self.hand_val = val


    def deal_first_cards(self, cards):
        '''
        Sets the first two cards for the start of the hand.
        '''
        self.cards = cards
        self.get_hand_val()


    def hit_me(self, new_card):
        '''
        Adds another card and updates hand value.
        '''
        self.cards.append(new_card)
        self.get_hand_val()