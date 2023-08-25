# Guessing game: pick a number from 1 to 100, have the players guess it.
# If the number's out of bounds, say so.
# On turn 1, if the number's within 10, say WARM; if not, say COLD
# On subsequent turns, if they're getting closer, say WARMER; otherwise, say
#    COLDER.
# When they get it right, announce it and the number of guesses.

from random import randint

cont = input('Would you like to play a game? (Y/N): ')[0]

while cont.lower() == 'y':
	print('Guess a WHOLE number between 1 and 100.')
	print("If you're close on the first guess, I'll tell you you're warm.")
	print("If you're not close, I'll tell you you're cold.")
	print("Then I'll tell you on later guesses if you're getting warmer or colder.")
	print('\n')

	# Generate random number.
	my_num = randint(1, 100)
	guesses = 0

	while True:
		# If it's the first guess, display a different string.
		if guesses == 0:
			input_str = 'Take your first guess: '
		else:
			input_str = 'Guess again: '

		# It makes me itchy that we haven't done exception handling here
		# (in case they enter a letter or something stupid) but okay.
		user_guess = int(input(input_str))

		# Check 0: 69
		if user_guess == 69:
			print('Nice!')

		# Check 1: If they're right, they're right. Break out of this while loop.
		if user_guess == my_num:
			if guesses == 0:
				print(f'Holy schnikes, you got it on the first guess!')
			else:
				print(f"Yay! You got it in {guesses + 1} guesses!")
			break
		# Check 2: If they're out of bounds. No.
		elif (user_guess < 1) or (user_guess > 100):
			print("No! That's out of bounds! Don't be silly!")
			continue
		else:
			# Check 3: If this is the first guess, establish warm vs. cold.
			if guesses == 0:
				if abs(user_guess - my_num) <= 10:
					print('Warm!')
				else:
					print('Cold!')
			# Check 4: If not the first guess, establish warmER vs. coldER (vs. the same I guess?)
			else:
				if abs(user_guess - my_num) < abs(last_guess - my_num):
					print('Warmer!')
				elif abs(user_guess - my_num) > abs(last_guess - my_num):
					print('Colder!')
				else:
					print('Same distance!')

		# Store the last guess and increment the counter.
		last_guess = user_guess
		guesses += 1

	# Do they want to play again?
	cont = input('Would you like to play again? (Y/N): ')[0]
# If they don't want to play again/ever, thank them for their time.
else:
	print('Thank you for playing!')