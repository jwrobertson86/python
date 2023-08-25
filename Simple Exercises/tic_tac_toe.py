# Tic tac toe: two-player game. Player 1 will choose X or O, then X will go first.
# Players will alternate placing X's and O's until one player wins, or until a draw
# is reached. Then the game begins anew.


##### GET YES OR NO #####
def get_yes_no(message):
	ans = ''

	print('')
	while ans not in ('y', 'n'):
		ans = input(message)[0].lower()
	print('')

	return ans


##### DISPLAY BOARD #####
def display_board(interior):
	print('')
	print('   |   |   ')
	print(' {} | {} | {} '.format(interior[0],interior[1],interior[2]))
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' {} | {} | {} '.format(interior[3],interior[4],interior[5]))
	print('   |   |   ')
	print('---+---+---')
	print('   |   |   ')
	print(' {} | {} | {} '.format(interior[6],interior[7],interior[8]))
	print('   |   |   ')
	print('')


##### GET PLAYER 1'S MARKER #####
def get_player1():
	xo = ''

	# Keep going until we get an X or an O.
	print('')
	while xo not in ('X', 'O'):
		xo = input('Player 1, will you be X or O? ')[0].upper()
	print('')

	print(f'Player 1 has chosen {xo}.')

	return xo


##### RANDOMLY CHOOSE THE FIRST PLAYER #####
def get_first_player():
	import random

	choice = random.random();

	if choice < 0.5:
		first_player = 'X'
	else:
		first_player = 'O'

	print(first_player + ' will go first.')
	return first_player


##### ASK WHERE THE NEXT MOVE WILL BE MADE #####
def get_place(turn):
	entry = 0

	# We only want integers in the range of 1-9 inclusive.
	while entry not in range(1, 10):
		entry = int(input(turn + ', select your spot based on the numpad: ')) # try-except block will eventually be needed.

	return str(entry)


##### DETERMINE IF THE MOVE IS VALID. #####
def valid_input(next_place, board_list):
	# First, find the index of next_place.
	ind = number_key.index(next_place)

	# If the board has a space there, we're good. If not...nah.
	return board_list[ind] == ' '


##### MAKE THE MOVE #####
def take_turn(letter, next_place, board_list):
	# First, find the index of next_place.
	ind = number_key.index(next_place)

	# Replace the character then return the board.
	board_list[ind] = letter
	return board_list


##### DETERMINE IF THERE IS A WINNER #####
def is_solved(interior):
	valid_solutions = [ (0, 1, 2), 
						(3, 4, 5),
						(6, 7, 8),
						(0, 3, 6),
						(1, 4, 7),
						(2, 5, 8),
						(0, 4, 8),
						(2, 4, 6),
					  ]

	for a,b,c in valid_solutions:
		if (interior[a] == interior[b] == interior[c]) and (interior[a] != ' '):
			return (True, interior[a]) # return the winner.

	return(False, ' ')


##### IS THE BOARD FULL? #####
def is_full(interior):
	return ' ' not in interior


##### MAIN FUNCTION #####
cont = get_yes_no('Would you like to play a game? (Y/N): ')

while cont == 'y':
	number_key = ['7','8','9','4','5','6','1','2','3']

	print('Welcome to Tic Tac Toe!')
	print("The rules are simple: Take turns placing X's and O's in a 3x3 grid")
	print('until one has placed three in a row, or until the grid is filled.')
	print('')
	print("You'll choose your grid position using the number pad, like so:")
	display_board(number_key)
	print('As a wise person (?) once said: the only winning move is not to play!')

	player1 = get_player1()
	turn = get_first_player()

	done = False
	board_list = [' ',' ',' ',' ',' ',' ',' ',' ',' '] # Could have been [' '] * 9!

	while done == False:
		# Get the player's input.
		if player1 == turn:
			player_name = 'Player 1'
		else:
			player_name = 'Player 2'

		next_place = get_place(player_name)

		# If it's not valid (if there's something already there), try again.
		if not valid_input(next_place, board_list):
			continue
		else:
			# Otherwise, place the letter.
			board_list = take_turn(turn, next_place, board_list)

			# Check for a winner.
			is_winner = is_solved(board_list)

			if is_winner[0]:
				done = True
				print(f'{is_winner[1]} HAS WON!')
			else:
				# Check to see if we have a full table.
				done = is_full(board_list)
				if done:
					print('Game Over! The board filled up.')

		# Display the board at the end of the turn.
		display_board(board_list)

		# Change the letter.
		if turn == 'X':
			turn = 'O'
		else:
			turn = 'X'

	cont = get_yes_no('Would you like to play again? (Y/N): ')