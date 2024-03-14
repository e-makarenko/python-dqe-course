import csv
from collections import Counter

class TextAnalyser:
    def __init__(self, text):
        self.text = text

    def count_words(self):
        # convert text to lower and split it to words
        words = self.text.lower().split()

        cleaned_words = []
        for word in words:
            cleaned_word = ""
            # check if the current character is alphanumeric with isalnum() method, if yes add it to the cleaned word
            for character in word:
                if character.isalnum():
                    cleaned_word += character
            cleaned_words.append(cleaned_word)

        word_counts = Counter(cleaned_words)
        return word_counts

    def count_letters(self):
        letters = ''.join(filter(str.isalpha, self.text))
        # convert all letters to lower case and count them
        lower_letters = letters.lower()
        total_letters = Counter(lower_letters)

        upper_letters = Counter(filter(str.isupper, self.text))

        # calculate percentage of upper case letters for each letter
        percentage = {}
        for letter in total_letters:
            # get the value of the uppercase version of the letter from the upper_letters dictionary (if no value, default value is 0)
            percentage[letter] = upper_letters.get(letter.upper(), 0) / total_letters[letter] * 100

        # create list of tuples containing information about each letter to save it to the csv
        letter_counts = []
        for letter in total_letters:
            letter_counts.append(
                (letter, total_letters[letter], upper_letters.get(letter.upper(), 0), percentage[letter]))

        return letter_counts

    # method to save the results to csv file
    def save_to_csv(self, filename, data, is_header=False):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            if is_header:
                headers = ['letter', 'count_all', 'count_uppercase', 'percentage']
                writer.writerow(headers)
            writer.writerows(data)
