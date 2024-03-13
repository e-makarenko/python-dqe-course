import os
import sys
import datetime

# add path to the directory where text processing function from HW 4 is defined
sys.path.insert(0, 'C:\\Users\\aa.emakarenko\\PycharmProjects\\python-dqe-course\\python-dqe-course\\module_4_functions')

# import the text processing function from the specified module
from task_module_3 import process_text


class Record:
    def publish(self):
        self.text = process_text(self.text)
        with open('feed.txt', 'a') as file:
            file.write(self.publish_header)
            file.write(self.get_record_content())
            file.write('\n\n')


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

    # method to process the file
    def process_file(self):
        with open(self.filepath, 'r') as file:
            # read all the lines and store them in the list
            lines = file.readlines()

        for line in lines:
            record_type, *args = tuple(line.rstrip().split('; '))

            # depending on the record type create instance of the respective class
            if record_type.lower() == 'news':
                record = News(*args)
                record.publish()
            elif record_type.lower() == 'ad':
                record = PrivateAd(*args)
                record.publish()
            elif record_type.lower() == 'song':
                record = SongOfTheDay(*args)
                record.publish()
            else:
                print(f"Invalid record type: {record_type}")
                return False

        # if all lines correctly processed remove the input file from directory
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
        return self.text + '\n' + 'Valid until: ' + self.exp_date.strftime("%d/%m/%Y") + ', ' + str(
            days_left) + ' days left'


class SongOfTheDay(Record):
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.text = f"Song name: {self.song}\nArtist: {self.artist}\n"
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

        record.publish()

# if user chooses to provide input from file an instance of the class FileReader with filepath as the argument
elif type_of_input == 'f':
    reader = FileReader(filepath)
    # if process_file method fails the error message is provided
    if not reader.process_file():
        print("File could not be processed because of incorrect format.")
