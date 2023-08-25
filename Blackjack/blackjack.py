'''
Blackjack game main file.
'''

from os import system, name
from time import sleep #equivalent of pause()
import bj_classes
import bj_errors

##### CLEAR SCREEN #####
def clear():
    '''
    Simple screen-clearing routine.
    '''
    if name == 'nt': # Windows
        _ = system('cls')
    else: # Mac/Linux (os.name == 'posix')
        _ = system('clear')


##### GET ANY KEY TO CONTINUE #####
def get_any_key():
    '''
    Gets any key to continue.
    '''
    if name == 'nt': # Windows
        system('pause')
    else: # Mac/Linux (os.name == 'posix')
        system('read -s -n 1 -p "Press any key to continue..."')


##### STARTING DEAL #####
def starting_deal(cards, pc, dealer):
    '''
    Deal in the Player and Dealer.
    '''
    pc_cards = []
    dealer_cards = []

    # Player receives first card.
    pc_cards.append(cards.deal_card())

    # Dealer receives first card.
    dealer_cards.append(cards.deal_card())

    # Player receives second card.
    pc_cards.append(cards.deal_card())

    # Dealer receives second card.
    dealer_cards.append(cards.deal_card())

    # Send them out.
    pc.deal_first_cards(pc_cards)
    dealer.deal_first_cards(dealer_cards)


##### PLAYER LOOP #####
def player_turn(cards, pc, dealer):
    '''
    Loop for blackjack player.
    '''
    # Import game_state from global.
    global game_state

    display_game(pc, dealer, 'Player')

    while True: # Outer loop is for gameplay.
        while True: # Inner loop is for input.
            pc_choice = input("Will you (H)it or (S)tand? ").upper()[0]

            if pc_choice not in ('H', 'S'):
                continue
            else:
                break

        if pc_choice == 'H':
            pc.hit_me(cards.deal_card())

            clear()
            display_game(pc, dealer, 'Player')

            if pc.hand_val > 21: # It's already been checked for soft/hard Aces
                game_state['winner'] = 'Dealer'
                print('You went bust!')
                break
            elif pc.hand_val == 21:
                print('You have 21! Hooray!')
                sleep(2) # Pause two seconds before clearing the screen.
                break # Automatically stands on 21.
            else:
                continue # Offers another choice.
        else: # i.e., pc_choice == 'S'
            break


##### DEALER LOOP #####
def dealer_turn(cards, pc, dealer):
    '''
    Loop for blackjack dealer.
    '''
    global game_state

    # Display the board for the first time.
    display_game(pc, dealer, 'Dealer')

    while True:
        cur_hand = dealer.hand_val # To distinguish from the new value.

        if cur_hand <= 17: # Dealer MUST hit on 17 or under.
            print('Dealer must hit.')
            dealer.hit_me(cards.deal_card())
        else: # Dealer MUST stand on 18 or over.
            print('Dealer must stand.')
            break

        sleep(2) # Pause two seconds before clearing the screen.
        display_game(pc, dealer, 'Dealer')

        # Check the new hand value.
        if dealer.hand_val > 21:
            game_state['winner'] = 'Player'
            print('Dealer went bust!')
            break
        elif dealer.hand_val == 21:
            print('Dealer has 21! Uh-oh!')
            break
        else:
            continue


##### BLACKJACK CHECK #####
def blackjack_check(pc, dealer):
    '''
    Checks at the start of the hand for blackjacks. If either the player or the dealer
    has a blackjack, the hand is over and the blackjack holder wins. If BOTH participants
    have blackjacks, it's a push.
    '''
    # Import game_state from global.
    global game_state

    # Get the hand values. If they're 21, given that we only have two cards, it's blackjack.
    pc_blackjack = (pc.hand_val == 21)
    dealer_blackjack = (dealer.hand_val == 21)

    # Check our logic. If neither are 21, just leave. If both are 21, it's a push.
    # If only one is 21, we have a winner. Any 21s denote a game-over state.
    if (not pc_blackjack) and (not dealer_blackjack):
        pass
    else:
        game_state['blackjack'] = True
        display_game(pc, dealer, 'Blackjack') # Display the cards since we haven't done that yet.

        if pc_blackjack and dealer_blackjack:
            print('DOUBLE BLACKJACK!!! WHOA!!!')
            game_state['winner'] = 'Push'
        elif pc_blackjack:
            print('YOU GOT A BLACKJACK!!!')
            game_state['winner'] = 'Player'
        elif dealer_blackjack: # Could be else but I want to be clear.
            print('Dealer blackjack! =(')
            game_state['winner'] = 'Dealer'


##### CHECK GAME STATE #####
def check_scores(pc, dealer):
    '''
    Checks the game scores to determine if any win or loss conditions have been met.
    '''
    # Import game_state from global.
    global game_state

    if pc.hand_val == dealer.hand_val:
        game_state['winner'] = 'Push'
    elif pc.hand_val > dealer.hand_val:
        game_state['winner'] = 'Player'
    elif pc.hand_val < dealer.hand_val:
        game_state['winner'] = 'Dealer'


##### OUTPUT CURRENT GAME STATE #####
def display_game(pc, dealer, turn):
    '''
    Outputs current state of blackjack game.
    '''
    pc_cards = str(pc)
    dealer_cards = str(dealer)

    # If it's the player's turn, obscure the second card. Since we don't know if
    # the second card is a 10 or not, just disconnect and reconnect the list.
    if turn == 'Player':
        card_list = dealer_cards.split(', ')
        card_list[1] = 'XX (??)'
        dealer_cards = ', '.join(card_list)

    clear()
    print("Dealer's Hand: " + dealer_cards)
    print("")
    print("Your Hand: " + pc_cards)
    print("")


##### GET BET FROM PC #####
def get_bet(pc):
    '''
    Gets a wager from the player and checks to ensure the player has sufficient funds.
    '''
    while True:
        # Action 1: Get the bet amount; make sure it's an int.
        try:
            bet = int(input(f"Enter bet amount (Max: ${pc.bankroll:.2f}): "))
        except TypeError:
            print("Error! You probably didn't put an integer in!")
            continue # Yes, I could put the next try block into an else but this seems cleaner.
        except Exception as e:
            print(f'Error! Something else weird happened! ({e})')
            continue

        # Action 2: Place the bet; make sure it's not too much.
        try:
            pc.bet(bet)
        except bj_errors.BetTooLarge:
            print("Error! You don't have that much money!")
            continue
        except Exception as e:
            print(f'Error! Something else weird happened! ({e})')
            continue

        # Keeps looping until the bet is legal.
        break

    return bet


##### MAIN FUNCTION #####

# Welcome, explain the rules.
clear()

print("Welcome to Blackjack!")
print("")
print("The objective is to try to get as close to 21 points in your hand as")
print("possible without going over. The dealer will then try to do the same.")
print("The dealer must hit (take a card) on 17 and stand (refuse one) on 18.")
print("The player is under no such obligation.")
print("")
print("Face cards (J/Q/K) are worth 10, while Aces (A) can be worth 1 or 11.")
print("That means you can get a 21 on your first two cards. That's a blackjack!")
print("Blackjacks are the best hand in the game, and can only be tied by another")
print("blackjack.")
print("")
print("")
print("")

get_any_key()
clear()

pc = bj_classes.Player() # pc = player character
dealer = bj_classes.Player()

while True:
    # Fresh deck every round.
    cards = bj_classes.Deck()

    # Get the bet from the player.
    bet = get_bet(pc)

    # Deal the first two cards to each person.
    starting_deal(cards, pc, dealer)

    # Define game state as dictionary. This will be pulled into each subsequent
    # gameplay function, as the one true global variable. (Mostly to show I know
    # how global variables work in Python, because it's sort of iffy practice.)
    # This originally contained a game-over flag but it became superfluous once
    # I realized that any state other than N/A for winner was the game-over flag
    # as it was.
    game_state = {'winner': 'N/A', 'blackjack': False}

    while True:
        # First, check for blackjacks.
        blackjack_check(pc, dealer)

        # Exit early if we're already done.
        if game_state['winner'] != 'N/A':
            break

        # Player hit/stand loop. Displaying screen within. If player busts, it's
        # game over, dealer wins.
        player_turn(cards, pc, dealer)

        # Exit early if we're already done.
        if game_state['winner'] != 'N/A':
            break

        # Dealer hit/stand loop. Again, display screen within. Dealer must hit on 
        # 17/stand on 18+. Pause for 3 seconds after each move. Again, bust ends 
        # the game automatically.
        dealer_turn(cards, pc, dealer)

        # Exit early if we're already done.
        if game_state['winner'] != 'N/A':
            break

        # At dealer's turn end, if no other end condition's been met, check the scores.
        check_scores(pc, dealer)

        # Okay, now exit; we're definitely done.
        break

    # Check the winner. If player won with a blackjack, give them an extra 50%.
    # If they just plain old won, just give them their regular double bet back.
    # If a push, no harm, no foul. If the dealer won, you get nothing. In any
    # case, output a little message.
    if game_state['winner'] == 'Player':
        if game_state['blackjack']: # Blackjacks pay out an extra 50%. Because reasons.
            winnings = 2.5 * bet
        else:
            winnings = 2 * bet

        print(f'Congratulations, Player! You win ${winnings:.2f}!')
        pc.payout(winnings)
    elif game_state['winner'] == 'Dealer':
        print('Dealer wins. Sorry!')
    elif game_state['winner'] == 'Push':
        print('Push! Bet returned.')
        pc.payout(bet)

    print('')
    print(f'You now have ${pc.bankroll:.2f} in the bank.')
    print('')

    # Ask if they want to play again (i.e., [B]et or [Q]uit.)
    while True:
        play_again = input("(B)et again or (Q)uit? ").upper()[0]

        if play_again not in ('B', 'Q'):
            continue
        else:
            break

    if play_again == 'B':
        continue
    else: # i.e., play_again == 'Q'
        break
