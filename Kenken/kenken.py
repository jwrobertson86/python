# This is a KenKen hint generator. It will prompt the user for a series of parameters
# for a given KenKen block (i.e., combination of connected cells within a larger board).
# It will then generate a sequence of valid possible solutions based on the information
# provided.

# Imports
from os import system, name
import math

# These first two functions are copied from other projects; I may want to make this a tiny
# module eventually.

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


##### ADDITION ALGORITHM #####
def addSet(outputVal, maxVal, boxSize):
    '''
    Determines which combinations will produce a sum of outputVal given a maximum possible
    addend of maxVal and boxSize total addends.

    Example:  __ __ __  This is a three-cell box (boxSize = 3). If it has a notation of
             |__|__|__| "8+", that means outputVal = 8. If it came from, say, a 5x5 puzzle
                        then maxVal = 5.

    The function returns solutionSet, a list of lists containing possible solutions. These
    may then need to be pruned down based on what kinds of repeated numbers are permissible.
    In our example above, there are several possible solutions (5 + 2 + 1, 4 + 3 + 1, etc.)
    which will then be represented as [[5, 2, 1],
                                       [4, 3, 1], ...]
    '''

    # Create an empty list.
    solutionSet = list()
    
    # Determine the smallest number we need to search toward; this is where we stop in order
    # to avoid repeating sequences in different orders (e.g., [5, 2, 1] and [2, 5, 1]). In
    # this case, it's the output divided by the size of the box. (Consider that the closest
    # set of three addends for our example above is [3, 3, 2], and that 8 / 3 = 2.67)
    lastVal = math.ceil(outputVal / boxSize)
    
    # Start from the largest number possible (i.e., the size of the grid). We are going to
    # be subtracting this from our target value to determine what's leftover.
    for i in range(maxVal, lastVal - 1, -1):
        # Ignore any subtractions that would produce a negative number.
        if outputVal > i:
            # If we have only two numbers, then perform the subtraction. Otherwise, we need
            # to use recursion.
            if boxSize == 2:
                solutionSet.append([i, outputVal - i])
            else:
                # Recursion rules: we are now adding to outputVal - i, our max value is now
                # i (to prevent duplication), and our box size is reduced by one.
                solutionSubSet = addSet(outputVal - i, i, boxSize - 1)

                # If anything was returned, stick it on to the solution set.
                for a in solutionSubSet:
                    solutionSet.append([i] + a)
    
    return solutionSet


##### SUBTRACTION ALGORITHM #####
def subtractSet(outputVal, maxVal):
    '''
    Determines which combinations will produce a difference of outputVal given a maximum
    possible minuend of maxVal. Note that subtractions can only be two cells.

    Example:  __ __  If our subtraction problem has a notation of "2-", that means outputVal
             |__|__| = 2. If it came from, say, a 5x5 puzzle then maxVal = 5.

    The function returns solutionSet, a list of lists containing possible solutions. In our
    example above, there are several possible solutions (5 - 3, 4 - 2, 3 - 1), which will
    then be represented as [[5, 3], [4, 2], [3, 1]].
    '''

    # Create an empty list.
    solutionSet = list()
    
    # Our range of minuends is from the maximum value to one more than the output, in
    # descending order. The subtrahend in each case is just the difference between the
    # minuend (i) and the solution (outputVal).
    for i in range(maxVal, outputVal, -1):
        solutionSet.append([i, i - outputVal])
    
    return solutionSet


##### MULTIPLICATION ALGORITHM #####
def multiplySet(outputVal, maxVal, boxSize):
    '''
    Determines which combinations will produce a product of outputVal given a maximum
    possible multiplicand of maxVal and boxSize number of factors.

    Example:  __ __ __  This is a three-cell box (boxSize = 3). If it has a notation of
             |__|__|__| "24x", that means outputVal = 24. If it came from, say, a 6x6 puzzle
                        then maxVal = 6.

    The function returns solutionSet, a list of lists containing possible solutions. These
    may then need to be pruned down based on what kinds of repeated numbers are permissible.
    In our example above, there are several possible solutions (6 * 4 * 1, 6 * 2 * 2, etc.)
    which will then be represented as [[6, 4, 1],
                                       [6, 2, 2], ...]
    '''

    # Create an empty list.
    solutionSet = list()
    
    # Determine the smallest number we need to search toward; this is where we stop in order
    # to avoid repeating sequences in different orders (e.g., [6, 2, 2] and [2, 2, 6]). In
    # this case, it's the Nth root of the output value, where N is the size of the box.
    # (Consider that the closest set of three factors for our example above is [4, 3, 2],
    # and that 24 ^ (1/3) = 2.88)
    lastVal = math.ceil(outputVal ** (1 / boxSize))
    
    # Start from the largest number possible (i.e., the size of the grid). We are going to
    # be dividing this from our target value to determine what's leftover.
    for i in range(maxVal, lastVal - 1, -1):
        # Ignore any divisions that would produce a fractional number.
        if outputVal % i == 0:
            # If we have only two numbers, then perform the division. Otherwise, we need to
            # use recursion.
            if boxSize == 2:
                solutionSet.append([i, int(outputVal / i)]) # cast to int
            else:
                # Recursion rules: we are now multiplying to outputVal / i, our max value
                # is now i (to prevent duplication), and our box size is reduced by one.
                solutionSubSet = multiplySet(int(outputVal / i), i, boxSize - 1)
                
                # If anything was returned, stick it on to the solution set.
                for a in solutionSubSet:
                    solutionSet.append([i] + a)
    
    return solutionSet


##### DIVISION ALGORITHM #####
def divideSet(outputVal, maxVal):
    '''
    Determines which combinations will produce a quotient of outputVal given a maximum
    possible dividend of maxVal. Note that divisions can only be two cells.

    Example:  __ __  If our division problem has a notation of "2/", that means outputVal
             |__|__| = 2. If it came from, say, a 6x6 puzzle then maxVal = 6.

    The function returns solutionSet, a list of lists containing possible solutions. In our
    example above, there are several possible solutions (6 / 3, 4 / 2, 2 / 1), which will
    then be represented as [[6, 3], [4, 2], [2, 1]].
    '''

    # Create an empty list.
    solutionSet = list()
    
    # Our range of dividends is from the maximum value to the output, in descending order. 
    # The divisor in each case is just the result of dividing the dividend (i) and the
    # ultimate solution (outputVal).
    for i in range(maxVal, outputVal - 1, -1):
        
        # Ignore any divisions that would produce a fractional number.
        if i % outputVal == 0:
            solutionSet.append([i, int(i / outputVal)]) # cast to int
    
    return solutionSet


##### REPETITION REMOVAL ALGORITHM #####
def pruneRepeats(solutionSet, maxVal, numRepeats = 0, maxRepeats = 2):
    '''
    This function takes in a solutionSet from one of the [operation]Set functions and, based
    on the specified pattern of permitted repetitions, excludes any that violate the rules.

    For example, consider the example from help(multiplicationSet). Given outputVal = 24,
    maxVal = 6, and boxSize = 3, we have three possible solutions: [[6, 4, 1], [6, 2, 2],
    [4, 3, 2]]. However, in that example, all the cells were in a single row, meaning that
    no repetitions are permitted. Thus, we use the default values of numRepeats = 0 (meaning
    no repetitions are allowed) and maxRepeats = 2 (meaning any sets of 2 or more of the
    same number are disallowed). This will remove [6, 2, 2] and leave us with [[6, 4, 1],
    [4, 3, 2]].

    By contrast, consider a box shaped like  __ __ . In this case, it is possible to have
                                            |__|__|  one set of numbers repeated (in the
                                               |__|  left and bottom cells). Thus, we can
                                                     have numRepeats = 1, while maxRepeats
    remains 2. For the solution set above, now no possibilities are pruned and all three
    solutions will be returned intact.

    We can get into the weeds with other examples of what's possible, and it's likely there
    are edge cases not considered by this algorithm. However, this should cover most
    scenarios one is likely to encounter with a normal kenken puzzle.
    '''

    # Sentinel value that is reset every time a solution is removed.
    remove = False

    # New copy of solutionSet to be pruned and returned.
    newSolutionSet = solutionSet.copy() # the .copy() is vital, turns out!
    
    for sol in solutionSet:
        # Count each number in the solution.
        counts = list()
        for i in range(maxVal, 0, -1):
            counts.append(sol.count(i))
        
        # If there are more than the permitted count of any given number (i.e., maxRepeats),
        # remove.
        if [i for i in counts if i > maxRepeats]:
            remove = True
        
        # If there are more than the permitted number of repeats (i.e., numRepeats), remove.
        # Note that we are looking for i >= maxRepeats here because here we're counting
        # legal repetitions.
        if len([i for i in counts if i >= maxRepeats]) > numRepeats:
            remove = True
        
        # Prune and reset.
        if remove:
            newSolutionSet.remove(sol)
            remove = False
    
    return newSolutionSet


##### PRINT OUT THE SOLUTIONS #####
def outputSolution(outputVal, operator, solutionSet):
    '''
    Crafts a text output based on a given solutionSet.

    If any solutions are found, it will print outputVal followed by a list of each solution
    in descending order of their largest number.

    Example: in the "3-" scenario presented in subtractSet, we will have an output of:

    3 = 
        5 - 3
        4 - 2
        3 - 1

    If no valid solutions are found (which is possible despite the guardrails in place), a
    simple text message will say so.
    '''

    # Base strings.
    outputString = str(outputVal) + ' = '
    joinString = ' ' + operator + ' '
    
    # PEP8: empty lists are False, so we can use boolean testing to determine what to do.
    print("")
    if solutionSet:
        print(outputString)
        
        # String multiplication and addition remains hilarious to me as someone who grew up
        # on C and its derivatives.
        for a in solutionSet:
            print(' ' * len(outputString) + joinString.join(map(str, a)))
    else:
        print('No solutions found. Check your parameters to ensure their validity.')

    print("")

##### HELP FUNCTION #####
def explain_kenken():
    clear()

    print("KenKen is a number-based logic puzzle akin to Sudoku. You're allowed one")
    print("number each from 1-N in each row or column, where N is the length of a row/")
    print("height of a column.")
    print("")
    print(" __" * 5)
    for i in range(0,5):
        print("|__" * 5 + "|")
    print("")
    print("This is a 5x5 puzzle. Within this puzzle, instead of mini-squares within which")
    print("only one of each number is allowed, kenken uses math-based boxes to limit")
    print("possibilities and create its logic puzzle. These boxes will be marked with a")
    print("number and an operator in their top-left corner: for example, '15+' means that")
    print("the numbers in the box must add up to 15. '2/' means that the largest number")
    print("divided by the smallest number must equal 2. And so forth.")
    print("")
    print("These boxes can contain the results of addition (+), subtraction (-),")
    print("multiplication (*), or division (/), and come in a variety of possible shapes.")
    print("")
    print("")

    get_any_key()
    clear()

    print(" __ __ __")
    print("|__|__|__| One possibility is that all cells are in a single row or column.")
    print("           Because of the rules of the game, you cannot have any repeated")
    print("numbers in here. All subtractions and divisions are only two cells long and")
    print("appear in a single row/column by definition. Addition and multiplication can")
    print("get more complicated.")
    print("")
    print(" __ __")
    print("|__|__| This is a simple example of a box with cells across multiple rows")
    print("|__|    and columns. Because of this, we could potentially have the same number")
    print("        in the rightmost and the bottom-most cells. Thus, one repetition")
    print("consisting of two matching numbers is possible. Larger, more advanced puzzles")
    print("can contain larger boxes, able to legally hold multiple pairs of numbers, or")
    print("even triplicates of numbers, but these are rare. By the time you run into")
    print("those, you probably won't need this explanation anymore.")
    print("")
    print("This should be enough information to use the program.")
    print("")
    print("")

    get_any_key()

##### MAIN FUNCTION #####

# Introduce ourselves.
clear()

print("Welcome to the KenKen Possibility Producer!")
print("")
print("This will take in various parameters describing a single box within a kenken puzzle")
print("And determine what possible ways you could arrive at the solution it asks for.")
print("")
print("Would you like a further illustration of some examples, or to just get on with it?")
print("")
print("")

# Determine if we provide help before getting our parameters.
while True:
    response = input("(H)elp or (C)ontinue: ").upper()[0]

    if response not in ('H', 'C'):
        print("Invalid response!")
        continue
    else:
        break

# If requested, give them that help.
if response == 'H':
    explain_kenken()

# Now, carry on. First things first, we need to know how big the puzzle is. This will,
# in principle, be a positive integer between 3 and 9. (I suppose it could be bigger but
# I've never seen a kenken bigger than 9x9.)
while True:
    clear()

    smallestKenKen = 3
    largestKenKen = 9

    maxVal = 0
    while ((maxVal < smallestKenKen) or (maxVal > largestKenKen)):
        try:
            maxVal = int(input("How big is the puzzle (e.g., '5' for an 5x5)? "))
        except ValueError:
            print("Error: Non-numeric value detected.")
        except:
            print("Error: Unknown problem detected.")
        else:
            if ((maxVal < smallestKenKen) or (maxVal > largestKenKen)):
                print(f"Error: KenKen puzzles must be between {smallestKenKen}x"\
                      f"{smallestKenKen} and {largestKenKen}x{largestKenKen}.")

    # Next, which operation are we performing? The operator must necessarily be one of four
    # values: '+', '-', '*', or '/'
    possibleOps = ('+', '-', '*', '/') # a tuple because we don't want to change it
    operator = ''

    # The operator should also be precisely one character long.
    while ((operator not in possibleOps) or (len(operator) != 1)):
        operator = input("What operation is being performed (+, -, *, or /)? ")

    # Next, based on which operation we're performing, we may or may not need further
    # information. Specifically, for addition and multiplication, we'll need to know
    # the size of the box, and information about repetitions.
    if operator in ('-', '/'):
        boxSize = 2
    else:
        boxSize = 0
        while (boxSize < 2):
            try:
                boxSize = int(input("How many cells are in the box? "))
            except ValueError:
                print("Error: Non-numeric value detected.")
            except:
                print("Error: Unknown problem detected.")
            else:
                if (boxSize < 2):
                    print("Error: Box must contain at least two cells.")

    # If we have more than two boxes, we need to know how they're arranged. This is a
    # potentially messy operation, so in lieu of that, we're just gonna ask about permitted
    # repetitions, because that's probably way easier than figuring it out based on some
    # complicated pattern of entering cells.

    # First, we'll ask how many sets of repeated numbers can exist in the box. For example,
    # [8, 6, 1, 1] is one; [7, 7, 1, 1] is two.
    if (boxSize == 2):
        numRepeats = 0
    else:
        numRepeats = -1
        while ((numRepeats < 0) or (numRepeats > 3)):
            try:
                numRepeats = int(input("How many sets of repeated numbers may exist in "\
                                       "the box? "))
            except ValueError:
                print("Error: Non-numeric value detected.")
            except:
                print("Error: Unknown problem detected.")
            else:
                if ((numRepeats < 0) or (numRepeats > 3)):
                    print("Error: There are only 0-3 sets of repeated numbers in most "\
                          "kenkens.")

    # Then, iff numRepeats > 0, we need to know how many times any given number can be
    # repeated. Usually, it's 2. In fact, I'm going to set 2 as a default and only accept
    # 3 as an alternative because it's so unusual to even run into this scenario.
    if (numRepeats != 0):
        possibleRepeats = ('2', '3') # a tuple because we don't want to change it
        repeats = input("How many times may the same number be repeated in the box "\
                        "(default = 2; other valid answer = 3)? ")
        
        # It should also be precisely one character long.
        if ((repeats not in possibleRepeats) or (len(repeats) != 1)):
            print("Invalid input. Using default of 2.")
            maxRepeats = 2
        else:
            maxRepeats = int(repeats)

    # Now that we have all that, we can finally see what solution we're meant to get. I
    # asked for all that other info first so we can account for obviously bad answers. For
    # example, you can't have three numbers that add up to 47, or two numbers that multiply
    # to 81 if the puzzle is anything less than 9x9.

    # The solution must be a positive integer (i.e., >= 1) regardless. However, for
    # different operations, we'll set the following loose boundaries:

    # Addition: minimum of 3 (i.e., 2 + 1); maximum of (N * boxes) - 1 for an NxN puzzle.
    # Subtraction: minimum of 1 (i.e., 2 - 1); maximum of N - 1
    # Multiplication: minimum of 2 (i.e., 2 * 1); maximum of (N ^ boxes) - 1
    # Division: minimum of 2 (i.e., 2 / 1); maximum of N

    # I'm aware that for the addition and multiplication it's more complicated than that,
    # but I don't know if I care enough to fuss with a more complicated formula based on
    # the two different repetition variables when the culling algorithm exists here.
    outputVal = 0
    lowerBound = 0
    upperBound = 0

    while True:
        try:
            outputVal = int(input("What is the solution value? "))
        except ValueError:
            print("Error: Non-numeric value detected.")
        except:
            print("Error: Unknown problem detected.")
        else:
            match operator:
                case '+':
                    lowerBound = 3
                    upperBound = (maxVal * boxSize) - 1
                case '-':
                    lowerBound = 1
                    upperBound = maxVal - 1
                case '*':
                    lowerBound = 2
                    upperBound = (maxVal ** boxSize) - 1
                case '/':
                    lowerBound = 2
                    upperBound = maxVal

            if (outputVal < lowerBound) or (outputVal > upperBound):
                print("Error: Solution appears out of bounds. Check parameters and try "\
                      "again.")
                continue
            else:
                break

    # Okay, we finally have everything. Now, we just need to run the actual algorithms. Yes,
    # the '+' and '*' could be combined into a single line but I prefer this for the sake
    # of readability.
    match operator:
        case '+':
            # Call the addition algorithm.
            solutionSet = addSet(outputVal, maxVal, boxSize)
            
            # Cull repeats.
            solutionSet = pruneRepeats(solutionSet, maxVal, numRepeats, maxRepeats)
        case '-':
            # Call the subtraction algorithm. There will be no repeats.
            solutionSet = subtractSet(outputVal, maxVal)
        case '*':
            # Call the multiplication algorithm.
            solutionSet = multiplySet(outputVal, maxVal, boxSize)
            
            # Cull repeats.
            solutionSet = pruneRepeats(solutionSet, maxVal, numRepeats, maxRepeats)
        case '/':
            # Call the division algorithm. There will be no repeats.
            solutionSet = divideSet(outputVal, maxVal)

    # Finally, print out our findings.
    outputSolution(outputVal, operator, solutionSet)

    # Now, do we want to go again?
    while True:
        run_again = input("Run again? (Y/N): ").upper()[0]

        if run_again not in ('Y', 'N'):
            continue
        else:
            break

    if run_again == 'Y':
        continue
    else: # i.e., run_again == 'N'
        break
