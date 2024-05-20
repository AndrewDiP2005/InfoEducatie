from colorama import init, Fore, Style
from sys import stdout
# Global variables
numberOfRounds = ''
numberOfLetters = ''
with open('WordsClassic.txt', 'r') as f:
    words = [word.strip() for word in f]
    words_dev = words[:]

def DisplayIntro() -> None:
    from time import sleep
    print('Welcome to WORDLEarn!\n- by Andrei Iaz!')
    # sleep(2)
    print(f'There are {len(words)} words in my dictionary\n')
    # sleep(1)
    init()                                  # asta e de la Colorama
    times = [1,1,1,1] # [3, 3, 5, 6]        # timpii de așteptare
    g = Fore.GREEN
    y = Fore.YELLOW
    rst = Style.RESET_ALL
    texts = [
                'For each guess, please write the following:',
                'Trial word: the word you tried, in lowercase',
                'Order(gyb): the order of colours (also lowercase)',
                f'With: g = {g + 'green' + rst}, y = {y + 'yellow' + rst}, b = black/grey'
            ]
    for line, secs in zip(texts, times):
        print(line)
        # sleep(secs)
    print('For example, if Wordle says:')
    stdout.write(g + 'c' + rst)
    stdout.write(    'r' + rst)
    stdout.write(y + 'a' + rst)
    stdout.write(g + 'n' + rst)
    stdout.write(    'e' + rst)
    print()
    print('Then you should input:')
    print('Trial word: crane')
    print('Order(gyb): gbygb')
    input('Ok? ')

def isPositiveValidNumber(value: str) -> bool:
    """
        Checks if the argument is a valid positive integer.
    """

    if value.isdigit():
        return int(value) > 0
    else:
        return False

def getRoundsAndLetters() -> tuple[int, int]:
    """
        Returns the number of rounds and the number of letters, as a tuple of two ints.
        Assumes that this is a classical game of Wordle, where there are 5 letters per word.
    """

    rounds = input('How many rounds? ')
    while not isPositiveValidNumber(rounds):
        rounds = input('Error: invalid number!\nHow many rounds? ')
    return int(rounds), 5

def updateWordList(word: str) -> None:
    """
    This is a maintenance class function, do not tamper with it.
    It checks if a word is in the words_dev global set (O(1)), and adds it if it's not.
    Additionally, it notifies the user at the interface about this.
    """
    global words_dev
    if word not in words_dev:
        words_dev = sorted(set(words_dev + [word]))
        with open('WordsClassic.txt', 'w') as f:
            f.writelines('\n'.join(words_dev))
        print(f'I learned a new word!\nNew total word list length: {len(words_dev)}')

def getTestedWord() -> str:
    """
    Checks if the given word has the valid number of letters.
    The check is made against the global number of letters (5 letters).
    """

    global numberOfLetters
    testedWord = input('Trial word: ')
    while len(testedWord) != numberOfLetters:
        testedWord = input('Error! Invalid word!\nTrial word: ')
    return testedWord

def isValidCode(code: str) -> bool:
    global numberOfLetters
    correctOrderLength = (len(code) == numberOfLetters)
    correctLetterCount = (code.count('b') + code.count('g') + code.count('y') == 5)
    return correctLetterCount and correctOrderLength

def getResultCode() -> str:
    global numberOfLetters
    resultCode = input('Order(gyb): ')
    while not isValidCode(resultCode):
        resultCode = input('Error! Invalid code!\nOrder(gyb): ')
    return resultCode

def DisplayProgress(prev: int, new: int) -> None:
    print(f'New length: {new}')
    p = round((prev - new) / prev * 100, 2)
    print(f'This is a {p}% shortening!')
    if int(p) > 95:
        print('Lucky guess ... or good choice!')

def updateCorrectStats(stat: str) -> None:
    with open('CorrectStats.txt', 'a') as stats:
        stats.write(stat)

# main function, not wrapped to avoid global imports
DisplayIntro()
numberOfRounds, numberOfLetters = getRoundsAndLetters()
for i in range(numberOfRounds):
    prevLength = len(words)
    stdout.write(f"\nGUESS {str(i+1)}\n\n")
    testedWord = getTestedWord()
    resultCode = getResultCode()
    if testedWord not in words_dev:
        updateWordList(testedWord)

    for j, letter, colour in zip(range(numberOfLetters), testedWord, resultCode):
        if colour == 'g':
            words = [w for w in words if w[j] == letter]
        elif colour == 'y':
            words = [w for w in words if letter in w and w[j] != letter]
        elif colour == 'b':
            sameLetterOnGreenPos = list(zip(testedWord, resultCode)).count((letter, 'g'))
            sameLetterOnYellowPos = list(zip(testedWord, resultCode)).count((letter, 'y'))
            aux = sameLetterOnGreenPos + sameLetterOnYellowPos  # we could count 'y' only [:j]
            words = [w for w in words if w.count(letter) == aux]

    if len(words) > 7: print(str(words[:7])[:-1] + ', ...]\n')
    else: print(words[:7])

    if len(words) == 0:
        print('I don\'t know the answer!')
        updateCorrectStats(',?')
        unknownSolution = input('What was the solution? ')
        if unknownSolution in words_dev:
            print('But I knew that one!!!')  # this should be very alarming
        else:
            updateWordList(unknownSolution)
        break
    elif len(words) == 1:
        stat = ',0'
        init()
        g, rst = Fore.GREEN, Style.RESET_ALL
        print('My guess:', g + str(words[0]) + rst)
        print('Congrats! There\'s only one possible solution left!')
        if input('Was that the solution? (Y/N) ').upper() == 'Y':
            print('I\'m glad, bye!')
            stat = ',1'
        else:
            unknownSolution = input('What was the solution? ')    # also very alarming
            if unknownSolution in words_dev:
                print('But I knew that one!')
            else:
                print('Didn\'t know it')
                updateWordList(unknownSolution)
        updateCorrectStats(stat)
        break

    newLength = len(words)
    DisplayProgress(prevLength, newLength)

exitcode = input('Press any hotkey to exit...')