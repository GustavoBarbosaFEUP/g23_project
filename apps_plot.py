from flask import render_template, session
from datafile import filename
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objs as go
import plotly
import json
from collections import Counter

def apps_plot():
    engine = create_engine('sqlite:///data/FashionDesigners.db')
    
    # Chart 1: Number of collections per year
    collections = pd.read_sql('Collections', con=engine)
    years = collections['release_year'].tolist()
    year_count = Counter(years)
    sorted_years = sorted(year_count.keys())
    collection_counts = [year_count[year] for year in sorted_years]

    fig1 = go.Figure(data=[
        go.Bar(x=sorted_years, y=collection_counts, marker_color='purple')
    ])
    fig1.update_layout(
        title='Number of Collections per Year',
        xaxis_title='Year',
        yaxis_title='Number of Collections'
    )
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Chart 2: Top 5 Designer Nationalities
    designers = pd.read_sql('Designers', con=engine)
    nationalities = designers['nationality'].tolist()
    nationality_count = Counter(nationalities)
    top5_nationalities = nationality_count.most_common(5)
    top_nationalities = [item[0] for item in top5_nationalities]
    nationality_values = [item[1] for item in top5_nationalities]

    fig2 = go.Figure(data=[
        go.Bar(x=top_nationalities, y=nationality_values, marker_color='skyblue')
    ])
    fig2.update_layout(
        title='Top 5 Designer Nationalities',
        xaxis_title='Nationality',
        yaxis_title='Number of Designers'
    )
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Chart 3: Top 5 Contributors by Contribution Percentage
    designers_collections = pd.read_sql('Designers_collections', con=engine)
    
    top_contributors = (
        designers_collections.groupby('designer_id')['contribution_percentage']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    # Merge with designer names
    top_contributors = top_contributors.merge(designers[['designer_id', 'name']], on='designer_id')

    fig3 = go.Figure(data=[
        go.Pie(labels=top_contributors['name'], values=top_contributors['contribution_percentage'])
    ])
    fig3.update_layout(
        title='Top 5 Contributors (by % Contribution)'
    )
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    # Chart 4: Fashion Shows Over Time (scatter)
    fashion_shows = pd.read_sql('Fashion_show', con=engine)
    fashion_shows['date'] = pd.to_datetime(fashion_shows['date'], errors='coerce')

    fig4 = go.Figure(data=[
        go.Scatter(
            x=fashion_shows['date'],
            y=fashion_shows['show_name'],
            mode='markers',
            marker=dict(color='blue', size=8),
            text=fashion_shows['venue']
        )
    ])
    fig4.update_layout(
        title='Fashion Shows Over Time',
        xaxis_title='Date',
        yaxis_title='Show Name'
    )
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("plot.html", 
                           graphJSON1=graphJSON1, 
                           graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3,
                           graphJSON4=graphJSON4,
                           ulogin=session.get("user"))


