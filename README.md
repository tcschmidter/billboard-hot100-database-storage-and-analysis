# Billboard Hot 100 database storage and data analysis
by Thomas Clayton Schmidter

- Scrapes the Billboard Weekly Hot 100 from 1958 to current day using BeautifulSoup
- Stores the data in a SQLite database
- Analyzes various trends in the Billboard Hot 100

## Database
### update.py
Scrapes data and updates the database
### billboard_hot100.db
Stores Date,Rank,Song,Artist of the Hot 100 songs for each week starting from 1958
## Analysis
### longest_running_songs.py
Determines the top 10 songs that have appeared in the Hot 100 for the most weeks
![image](https://github.com/user-attachments/assets/f520b96c-1a81-400f-80aa-f3f2f139a09e)
(up-to-date as of 2024-07-21)
packages: Plotly, pandas
### largest_gaps_in_weeks.py
Determines the top 10 songs with the largest gaps between instances of appearing in the Hot 100
![image](https://github.com/user-attachments/assets/d6f229b3-42d3-4ee4-b2da-82abce866bde)
(up-to-date as of 2024-07-21)
### initial_rank_vs_weeks.py
Displays box and whisker plots showing the correlation between the initial ranking of a song in the Hot 100 and the number of weeks in the Hot 100
![image](https://github.com/user-attachments/assets/1eb40574-9412-4844-af88-7eefe22ceba1)
(up-to-date as of 2024-07-21)
