import random
import requests

class GameLogic:
    @staticmethod
    def ColorCode(userInput: str, rightWord: str) -> str:
        uiLC = {L: userInput.count(L) for L in userInput}        # userinputLettersCount
        rwLC = {L: rightWord.count(L) for L in rightWord}        # rightwordLettersCount
        code: List[str] = ['_' for _ in range(len(rightWord))]
        for pos, letter in enumerate(userInput):
            if userInput[pos] == rightWord[pos]:        # those that are correct, for sure are G
                code[pos] = 'G'
                uiLC[letter] -= 1
                rwLC[letter] -= 1
            elif userInput[pos] not in rightWord:       # those that are nowhere, for sure are B
                code[pos] = 'B'

        for pos, letter in enumerate(userInput):
            if code[pos] != '_':                        # we already did something with this letter
                continue

            # this is a letter in userInput that has a different letter below it
            if rwLC[letter] > 0:                        # the letter is somewhere else => Y
                code[pos] = 'Y'
                uiLC[letter] -= 1
                rwLC[letter] -= 1
            else:                                       # the letter is nowhere else => B
                code[pos] = 'B'

        return ''.join(code)

    @staticmethod
    def load_words(language):
        words = []
        with open(f"data/{language}.txt", "r") as file:
            words = [line.strip() for line in file]
        return words

    @staticmethod
    def get_words_by_length(words, length):
        return sorted([word for word in words if len(word) == length])

    @staticmethod
    def is_valid_word(word, length):
        return len(word) == length and word.isalpha()

    @staticmethod
    def get_feedback(guess, target):
        return GameLogic.ColorCode(guess, target)

    @staticmethod
    def fetch_definition(word):
        api_key = '5991a4f1-f1a3-43a6-9a23-29d5b5597268'
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and 'shortdef' in data[0]:
                return data[0]['shortdef'][0]
        return "Definition not found"
