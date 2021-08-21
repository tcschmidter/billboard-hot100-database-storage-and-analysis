import requests
from bs4 import BeautifulSoup
import csv


link = "https://www.billboard.com/charts/hot-100/"

# date specifies the week of the billboard top 100
# if date is empty, the current week is accessed
date = ""

site = requests.get(f"{link}{date}")

soup = BeautifulSoup(site.text, "html.parser")

songs = soup.find_all("span", class_="chart-element__information__song")
songs = soup.select("li button span span.chart-element__information__song.text--truncate.color--primary")

artists = soup.find_all("span", class_="chart-element__information__artist")
artists = soup.select("li button span span.chart-element__information__artist.text--truncate.color--secondary")

song_names = [song.getText() for song in songs]
artist_names = [artist.getText() for artist in artists]
hot100 = [(song_names[i], artist_names[i]) for i in range(0, len(song_names))]

print(hot100)