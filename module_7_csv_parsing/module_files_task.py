import os
import sys
import datetime

# add path to the directory where text processing function from HW 4 is defined
sys.path.insert(0, 'C:\\Users\\aa.emakarenko\\PycharmProjects\\python-dqe-course\\python-dqe-course\\module_4_functions')
from task_module_3 import process_text

# import class for text analysis
from text_analyser import TextAnalyser

class Record:
    def publish(self):
        self.text = process_text(self.text)
        # create output directory to save output files to if it not exists
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'feed.txt'), 'a') as file:
            file.write(self.publish_header)
            file.write(self.get_record_content())
            file.write('\n\n')
        return self.text

class FileReader:
    def __init__(self, filepath = None):
        if filepath is None:
            # set default_path for input file using directory path and folder + file name
            default_path = os.path.join(os.path.dirname(sys.argv[0]), 'input', 'new_records.txt')
            if os.path.exists(default_path):
                self.filepath = default_path
            else:
                print('Default file path does not exist.')
                self.filepath = input('Please input correct file path for the input file: ')
        else:
            self.filepath = filepath

    # method to process the input file
    def process_file(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()

        # an empty list to keep all the texts returned by the publish method for each record in the file
        all_texts = []
        # depending on the record type create instance of the respective class
        for line in lines:
            record_type, *args = tuple(line.rstrip().split('; '))
            if record_type.lower() == 'news':
                record = News(*args)
            elif record_type.lower() == 'ad':
                record = PrivateAd(*args)
            elif record_type.lower() == 'song':
                record = SongOfTheDay(*args)
            else:
                print(f"Invalid record type: {record_type}")
                return False

            text = record.publish()
            all_texts.append(text)

        # create 1 text from all texts from the list and analyze it
        combined_text = ' '.join(all_texts)
        analyser = TextAnalyser(combined_text)
        word_counts = analyser.count_words()
        letter_counts = analyser.count_letters()
        # save csv files in the output directory
        analyser.save_to_csv('output/word_counts.csv', word_counts.items())
        analyser.save_to_csv('output/letter_counts.csv', letter_counts, is_header=True)

        # if all lines correctly processed remove the input file from directory
        if lines:
            os.remove(self.filepath)
        return True

class News(Record):
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.publish_header = 'News --------------------------\n'

    def get_record_content(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        return self.text + '\n' + self.city + ', ' + date

class PrivateAd(Record):
    def __init__(self, text, exp_date):
        self.text = text
        self.exp_date = datetime.datetime.strptime(exp_date, '%d/%m/%Y')
        self.publish_header = 'Private ad ---------------------------\n'

    def get_record_content(self):
        days_left = (self.exp_date - datetime.datetime.now()).days
        return self.text + '\n' + 'Valid until: ' + self.exp_date.strftime("%d/%m/%Y") + ', ' + str(days_left) + ' days left'

class SongOfTheDay(Record):
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.text = f"Song name - Artist\n{self.song} "-" {self.artist}\n"
        self.publish_header = 'Song of the day ----------------------\n'

    def get_record_content(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        return self.text + "\n" + date

# check if user has provided a file path in command line
# if yes, use it as the filepath, if not set filepath to None
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = None

type_of_input = input("Do you want to provide input from console('c') or file('f')?: ").lower()

while type_of_input not in ['c', 'f']:
    type_of_input = input("Invalid input type. Please choose if you want to provide input from console('c') or file('f')?: ").lower()

if type_of_input == 'c':
    all_texts = []
    while True:
        record_type = input("Please choose the record type ('news', 'ad', 'song') or 'exit' to quit: ").lower()
        if record_type == 'news':
            text = input("Enter text of the news: ")
            city = input("Enter city of the news: ")
            record = News(text, city)
        elif record_type == 'ad':
            text = input("Enter text of the ad: ")
            exp_date = input("Enter ad expiration date (dd/mm/yyyy): ")
            record = PrivateAd(text, exp_date)
        elif record_type == 'song':
            song = input("Enter song name: ")
            artist = input("Enter artist name: ")
            record = SongOfTheDay(song, artist)
        elif record_type == 'exit':
            break
        else:
            print("Invalid record type! Please enter 'news', 'ad', 'song' to add new record, or 'exit' to quit.")
            continue

        text = record.publish()
        all_texts.append(text)

    # perform same text analysis as process_file method
    combined_text = ' '.join(all_texts)
    analyser = TextAnalyser(combined_text)
    word_counts = analyser.count_words()
    letter_counts = analyser.count_letters()
    # save csv files in the output directory
    analyser.save_to_csv('output/word_counts.csv', word_counts.items())
    analyser.save_to_csv('output/letter_counts.csv', letter_counts, is_header=True)

# if user chooses to provide input from file an instance of the class FileReader with filepath as the argument is created
elif type_of_input == 'f':
    reader = FileReader(filepath)
    # if process_file method fails the error message is provided
    if not reader.process_file():
        print("File could not be processed because of incorrect format.")
