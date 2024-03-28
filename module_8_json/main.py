import os
import sys
import datetime
import json
import xml.etree.ElementTree as ET

# find current directory
current_file_dir = os.path.dirname(os.path.abspath(__file__))
# find root directory by going up a level
root_dir = os.path.dirname(current_file_dir)
# append the root directory to sys.path
sys.path.append(root_dir)

# import module for text processing
from module_4_functions.task_module_3 import process_text

# import module for text analysis
from module_8_json.text_analyser import TextAnalyser

# import module for database functionality
from database_manager import DatabaseManager


class Record:
    # class variable to store and process all records from 1 input
    all_records = []

    def __init__(self, text, record_type, params):
        # process text here to have it processed everywhere
        self.text = process_text(text)
        self.record_type = record_type
        self.params = params
        # update text with its normalized version
        self.params['text'] = self.text

        self.analyser = TextAnalyser(self.text)

        # add the instance of Record to all_records
        Record.all_records.append(self)

        # initialize class instance, create tables
        self.db = DatabaseManager()
        self.db.create_tables()

    def analyse_all_records():
        all_text = " ".join([record.text for record in Record.all_records])
        analyser = TextAnalyser(all_text)

        word_counts = analyser.count_words()
        letter_counts = analyser.count_letters()

        analyser.save_to_csv('output/word_counts.csv', word_counts.items())
        analyser.save_to_csv('output/letter_counts.csv', letter_counts, is_header=True)

    def write_text(self):
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'feed.txt'), 'a') as file:
            file.write(self.get_publish_header())
            file.write(self.get_record_content())
            file.write('\n\n')

    def get_publish_header(self):
        raise NotImplementedError("Method needs to be implemented in a child class")

    def get_record_content(self):
        raise NotImplementedError("Method needs to be implemented in a child class")

    def publish(self):
        Record.analyse_all_records()
        # add functionality of writing to the DB
        self.db.check_duplicate_and_insert(self.record_type, **self.params)
        self.write_text()


class FileReader:
    def __init__(self, filepath, filename):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input', self.filename)
        if not os.path.exists(self.filepath):
            print('Default file path does not exist.')
            self.filepath = input('Please input correct file path for the input file: ')

    def create_record(self, record_dict):
        record_type = record_dict.get('record_type', '').lower()
        args = record_dict.get('args', [])
        if record_type == 'news':
            return News(*args)
        elif record_type == 'ad':
            return PrivateAd(*args)
        elif record_type == 'song':
            return SongOfTheDay(*args)
        else:
            print(f"Invalid record type: {record_type}")
            return None

    def read_data(self):
        raise NotImplementedError("Method must be implemented in Child Class")

    def process_file(self):
        records = self.read_data()
        for record in records:
            self.create_record(record)

        for rec in Record.all_records:
            rec.publish()

        os.remove(self.filepath)

        return Record.all_records


class TxtFileReader(FileReader):
    def __init__(self, filepath=None):
        super().__init__(filepath=filepath, filename='new_records.txt')

    def read_data(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()

        records = []
        for line in lines:
            record_data = {}
            record_data["record_type"], *record_data["args"] = tuple(line.rstrip().split('; '))
            records.append(record_data)

        return records


class JSONReader(FileReader):
    def __init__(self, filepath=None):
        super().__init__(filepath=filepath, filename='new_records.json')

    def read_data(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)

        records = []
        for values in data.values():
            record_data = {}
            record_data['record_type'] = values.pop('record_type', '')
            record_data['args'] = list(values.values())
            records.append(record_data)

        return records


class XMLReader(FileReader):
    def __init__(self, filepath=None):
        super().__init__(filepath=filepath, filename='new_records.xml')

    def read_data(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        records = []
        for record_elem in root:
            record_data = {}
            record_data['record_type'] = record_elem.get('type', '').lower()
            record_data['args'] = [elem.text for elem in record_elem]
            records.append(record_data)

        return records


class News(Record):
    def __init__(self, text, city):
        super().__init__(text, 'news', {'city': process_text(city), 'text': text})

    def get_publish_header(self):
        return 'News --------------------------------\n'

    def get_record_content(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        return self.text + '\n' + self.params['city'] + ', ' + date


class PrivateAd(Record):
    def __init__(self, text, exp_date):
        exp_date_as_date = datetime.datetime.strptime(exp_date, '%d/%m/%Y')
        super().__init__(text, 'ad', {'exp_date': exp_date_as_date.strftime("%d/%m/%Y"), 'text': text})

    def get_publish_header(self):
        return 'Private ad ---------------------------\n'

    def get_record_content(self):
        exp_date_as_date = datetime.datetime.strptime(self.params['exp_date'], "%d/%m/%Y")
        days_left = (exp_date_as_date.date() - datetime.datetime.now().date()).days
        return self.text + '\n' + 'Valid until: ' + self.params['exp_date'] + ', ' + str(days_left) + ' days left'

class SongOfTheDay(Record):
    def __init__(self, song, artist):
        text = f"{song} - {artist}"
        super().__init__(text, 'song', {'text': text})

    def get_publish_header(self):
        return 'Song of the day ----------------------\nSong name - Artist: \n'

    def get_record_content(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        return self.text + "\n" + date


# check if user has provided a file path in command line
# if yes, use it as the filepath, if not set filepath to None
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = None

# user should pass type of input for news generation
type_of_input = input("Do you want to provide input from console('c') or file('f')?: ").lower()

while type_of_input not in ['c', 'f']:
    type_of_input = input("Invalid input. Please choose between console('c') or file('f')?: ").lower()

if type_of_input == 'c':
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

    for rec in Record.all_records:
        rec.publish()

elif type_of_input == 'f':
    file_type = input("What type of file will you be using? Enter 't' for txt, 'j' for JSON or 'x' for xml: ").lower()

    while file_type not in ['t', 'j', 'x']:
        file_type = input("Invalid file type. Please enter 't' for txt, 'j' for JSON, or 'x' for xml: ").lower()

    if file_type == 't':
        reader = TxtFileReader(filepath)
        reader.process_file()
        if not Record.all_records:
            print("File could not be processed due to incorrect format.")

    elif file_type == 'j':
        reader = JSONReader(filepath)
        reader.process_file()
        if not Record.all_records:
            print("JSON file could not be processed due to incorrect format.")

    elif file_type == 'x':
        reader = XMLReader(filepath)
        reader.process_file()
        if not Record.all_records:
            print("XML file could not be processed due to incorrect format.")
