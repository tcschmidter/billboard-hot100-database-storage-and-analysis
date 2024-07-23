import sqlite3
import pandas as pd
import plotly.graph_objects as go


def largest_gaps_chart():
    conn = sqlite3.connect('billboard_hot100.db')

    # query to find song appearances and calculate gaps in weeks
    query = '''
    WITH appearances AS (
        SELECT song, artist, date
        FROM hot100
        ORDER BY song, artist, date
    ),
    gaps AS (
        SELECT
            a.song,
            a.artist,
            a.date AS start_date,
            MIN(b.date) AS end_date,
            ROUND((JULIANDAY(MIN(b.date)) - JULIANDAY(a.date)) / 7.0) AS gap_weeks
        FROM appearances a
        LEFT JOIN appearances b
            ON a.song = b.song
            AND a.artist = b.artist
            AND b.date > a.date
        WHERE a.date < b.date
        GROUP BY a.song, a.artist, a.date
        HAVING gap_weeks IS NOT NULL
        ORDER BY gap_weeks DESC
    )
    SELECT song, artist, start_date AS first_missing_date, end_date AS last_seen_date, gap_weeks
    FROM gaps
    ORDER BY gap_weeks DESC
    LIMIT 10;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    # converts dates to datetime format
    df['first_missing_date'] = pd.to_datetime(df['first_missing_date'])
    df['last_seen_date'] = pd.to_datetime(df['last_seen_date'])

    # creates a bar chart with gap information
    fig = go.Figure()

    # sorts by gap_weeks from largest to smallest
    df = df.sort_values(by='gap_weeks', ascending=False)

    for i, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['gap_weeks']],
            y=[f"{row['song']} ({row['artist']})"],
            orientation='h',
            marker=dict(color='lightblue', line=dict(color='black', width=2)),
            text=[f"Gap of {int(row['gap_weeks'])} weeks"],
            textposition='inside',
            textfont=dict(color='black'),
            customdata=[(row['first_missing_date'].strftime('%Y-%m-%d'), row['last_seen_date'].strftime('%Y-%m-%d'))],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Gap of %{x} weeks<br>"
                "Start: %{customdata[0]}<br>"
                "End: %{customdata[1]}<extra></extra>"
            )
        ))

        # adds annotations for start and end dates
        fig.add_annotation(
            x=row['gap_weeks'] + 1,  # positions to the right of the bar
            y=f"{row['song']} ({row['artist']})",
            text=f"Start: {row['first_missing_date'].strftime('%Y-%m-%d')}<br>End: {row['last_seen_date'].strftime('%Y-%m-%d')}",
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(size=12, color='black'),
            align='left'
        )

    fig.update_layout(
        title_text="Top 10 Largest Gaps Between Appearances on the Hot 100",
        title_x=0.5,
        title_y=0.95,
        xaxis_title="Weeks",
        yaxis_title="Song and Artist",
        height=600,
        margin=dict(l=350, r=50, t=50, b=0),  # adjusts margins to fit text
        showlegend=False,  # hides the legend as all bars are the same color
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=2
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=2
        )
    )

    fig.show()


largest_gaps_chart()
