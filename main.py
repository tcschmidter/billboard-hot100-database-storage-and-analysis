import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import timedelta, datetime

LINK = "https://www.billboard.com/charts/hot-100/"
INITIAL_DATE = "1958-08-04"


# gets the dates of the weeks between two dates
def get_weeks(starting_date, ending_date):
    for n in range(0, int((ending_date - starting_date).days) + 1, 7):
        yield starting_date + timedelta(n)


#creates the database and the table if it doesn't exist
def create_database():
    conn = sqlite3.connect('billboard_hot100.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hot100 (
                    date TEXT,
                    rank INTEGER,
                    song TEXT,
                    artist TEXT,
                    PRIMARY KEY (date, rank)
                 )''')
    conn.commit()
    conn.close()


# adds the date, rank, song, artist of a weeks Hot 100 to the database
def insert_data(date, rank, song, artist):
    conn = sqlite3.connect('billboard_hot100.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR IGNORE INTO hot100 (date, rank, song, artist)
                     VALUES (?, ?, ?, ?)''', (date, rank, song, artist))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

# checks if the week's data already exists in database
def data_exists(date):
    conn = sqlite3.connect('billboard_hot100.db')
    c = conn.cursor()
    try:
        c.execute('''SELECT 1 FROM hot100 WHERE date = ? LIMIT 1''', (date,))
        exists = c.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Error checking data existence: {e}")
        exists = False
    finally:
        conn.close()
    return exists


# adds week of data for the missing date
def add_week(date_missing):
    if data_exists(date_missing):
        print(f"Data for {date_missing} already exists. Skipping...")
        return
    print(f"Adding data for {date_missing}...")
    try:
        site = requests.get(f"{LINK}{date_missing}", allow_redirects=True)
        site.raise_for_status()  # raise an error for bad responses
        soup = BeautifulSoup(site.text, "html.parser")

        # locate the text for song and artist name and append them to the hot100 list as tuples
        hot100 = []
        for ul in soup.find_all('ul'):
            li = ul.find('li')
            if li:
                h3 = li.find('h3', id='title-of-a-story')
                if h3:
                    hot100.append((h3.text.strip(), li.find('span').text.strip()))

        if not hot100:
            print(f"No data found for {date_missing}.")
            return
        
        # add week data to database
        for rank, (song, artist) in enumerate(hot100, start=1):
            insert_data(date_missing, rank, song, artist)

    except requests.RequestException as e:
        print(f"Request error for {date_missing}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# updates database with new weeks
def update():
    print("Updating database. This may take a while...")
    create_database()

    starting_date = datetime.strptime(INITIAL_DATE, "%Y-%m-%d")
    ending_date = datetime.today()

    for week_date in get_weeks(starting_date, ending_date):
        add_week(week_date.strftime("%Y-%m-%d"))

    print("Database updated.")


update()
