import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import timedelta, datetime, date

LINK = "https://www.billboard.com/charts/hot-100/"
DIRECTORY = "./hot100-data"

# date specifies the week of the billboard top 100
# the first week of Billboard Hot 100 is the week of August 4th, 1958
# if date is empty, the current week is accessed
INITIAL_DATE = "1958-08-04"
CURRENT_DATE = ""

# get weeks from start to end date
def get_weeks(starting_date, ending_date):
    for n in range(0, int((ending_date - starting_date).days) + 1, 7):
        yield starting_date + timedelta(n)

# checks for updates to ./hot100-data, and updates if necessary
def update():
    print("Updating files. This may take a while...")
    # if dir doesn't exist, create it
    try:
        os.makedirs(DIRECTORY)
    except OSError:
        if not os.path.isdir(DIRECTORY):
            raise


        starting_date = datetime.strptime(INITIAL_DATE, "%Y-%m-%d")
        ending_date = datetime.today()
        # go through each week, if file does not exist, create it and fill it with data
        for week_date in get_weeks(starting_date, ending_date):
            if not os.path.exists(DIRECTORY + "/" + week_date.strftime("%Y-%m-%d") + ".txt"):
                create_data_file(week_date.strftime("%Y-%m-%d"))

            # ************************
            # ************************
            # FIX: SOME FILES ARE EMPTY
            # ************************
            # ************************
    print("Files updated.")

def create_data_file(date_missing):
    site = requests.get(f"{LINK}{date_missing}")
    soup = BeautifulSoup(site.text, "html.parser")

    # finds all Hot 100 song names and puts them in a list
    songs = soup.find_all("span", class_="chart-element__information__song")
    songs = soup.select("li button span span.chart-element__information__song.text--truncate.color--primary")
    song_names = [song.getText() for song in songs]

    # finds all Hot 100 artist names and puts them in a list
    artists = soup.find_all("span", class_="chart-element__information__artist")
    artists = soup.select("li button span span.chart-element__information__artist.text--truncate.color--secondary")
    artist_names = [artist.getText() for artist in artists]

    # puts the song names and artists names together in a tuple
    hot100 = [(song_names[i], artist_names[i]) for i in range(0, len(song_names))]
    with open(DIRECTORY + "/" + date_missing + ".txt", 'w') as fp:
        fp.write('\n'.join("{}\t{}".format(song[0], song[1]) for song in hot100))
    print("Added file: " + DIRECTORY + "/" + date_missing + ".txt")

update()



