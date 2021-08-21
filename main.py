import requests
from bs4 import BeautifulSoup
import csv


link = "https://www.billboard.com/charts/hot-100/"

# date specifies the week of the billboard top 100
# if date is empty, the current week is accessed
date = "1970-01-01"

site = requests.get(f"{link}{date}")
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

print(hot100)
