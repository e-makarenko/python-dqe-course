import datetime


# main class for all record types
class Record:
    # method to write the record to a file
    def publish(self):
        with open('feed.txt', 'a') as file:
            file.write(self.publish_header)
            file.write(self.get_record_content())
            file.write('\n\n')


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
        self.publish_header = 'Song of the day ----------------------\n'

    def get_record_content(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        return 'Song name: ' + self.song + '\n' + 'Artist: ' + self.artist + '\n' + date


record_type = input("Please choose the record type ('news', 'ad', 'song'): ").lower()

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

else:
    print("Invalid record type!")

record.publish()
