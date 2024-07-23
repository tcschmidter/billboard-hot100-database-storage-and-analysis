import sqlite3
import pandas as pd
import plotly.express as px


def plot_box_and_whisker():

    conn = sqlite3.connect('billboard_hot100.db')

    # query to get the first rank and total weeks for each song
    query = '''
    SELECT song, artist, MIN(rank) AS first_rank, COUNT(DISTINCT date) AS total_weeks_in_hot_100
    FROM hot100
    GROUP BY song, artist;
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()

    # convers to numeric and handles errors
    df['first_rank'] = pd.to_numeric(df['first_rank'], errors='coerce')
    df['total_weeks_in_hot_100'] = pd.to_numeric(df['total_weeks_in_hot_100'], errors='coerce')

    df = df.dropna(subset=['first_rank', 'total_weeks_in_hot_100'])

    # groups by every 10 ranks
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']

    # bins the initial rankings
    df['rank_category'] = pd.cut(df['first_rank'], bins=bins, labels=labels, right=True)

    df['rank_category'] = pd.Categorical(df['rank_category'], categories=labels, ordered=True)

    # creates box and whisker plot
    fig = px.box(
        df,
        x='rank_category',
        y='total_weeks_in_hot_100',
        title='Distribution of Song Lifespan Based on Initial Ranking',
        labels={'rank_category': 'Initial Rank Range', 'total_weeks_in_hot_100': 'Total Weeks on Hot 100'},
        color='rank_category',
        boxmode='overlay',
        points='all'
    )


    fig.update_layout(
        xaxis_title='Initial Rank Range',
        yaxis_title='Total Weeks on Hot 100',
        title={'text': 'Distribution of Song Lifespan Based on Initial Ranking', 'x': 0.5, 'xanchor': 'center'},
        xaxis=dict(
            tickmode='array',
            tickvals=labels,
            ticktext=labels,
            title='Initial Rank Range',
            categoryorder='array',
            categoryarray=labels
        ),
        yaxis=dict(
            title='Total Weeks on Hot 100',
            autorange='reversed'
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(240,240,240,0.95)'
    )

    fig.show()


plot_box_and_whisker()
