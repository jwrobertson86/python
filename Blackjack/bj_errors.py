'''
Blackjack game exception file.
'''

class Error(Exception):
    '''Base error class'''
    pass

class BetTooLarge(Error):
    '''Bet too large class'''
    pass
