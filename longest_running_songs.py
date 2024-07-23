import sqlite3
import pandas as pd
import plotly.graph_objects as go


def longest_running_songs_table():
    conn = sqlite3.connect('billboard_hot100.db')

    # query to find the top 10 longest running songs with their first and last weeks
    query = '''
    SELECT song, artist, MIN(date) AS first_week, MAX(date) AS last_week, COUNT(DISTINCT date) AS total_weeks_in_hot_100
    FROM hot100
    GROUP BY song, artist
    ORDER BY total_weeks_in_hot_100 DESC
    LIMIT 10;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    # converts first_week and last_week to datetime format
    df['first_week'] = pd.to_datetime(df['first_week'])
    df['last_week'] = pd.to_datetime(df['last_week'])

    # creates a Plotly table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Song', 'Artist', 'First Week', 'Last Week', 'Total Weeks in Hot 100'],
            fill_color='paleturquoise',
            align='left',
            font=dict(size=14)
        ),
        cells=dict(
            values=[df['song'], df['artist'], df['first_week'].dt.strftime('%Y-%m-%d'),
                    df['last_week'].dt.strftime('%Y-%m-%d'), df['total_weeks_in_hot_100']],
            fill_color='lavender',
            align='left',
            font=dict(size=12),
            height=30  # sets a consistent height for cells
        )
    )])

    fig.update_layout(
        title_text="Top 10 Longest-Running Songs on the Hot 100",
        title_x=0.5,
        title_y=0.95,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    fig.show()


longest_running_songs_table()