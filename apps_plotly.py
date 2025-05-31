from flask import render_template, session
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

def apps_plotly():
    engine = create_engine('sqlite:///data/FashionDesigners.db')
    
    # Chart 1: Collections per Year
    collections = pd.read_sql('Collections', con=engine)
    years = collections['release_year'].tolist()
    df_years = pd.DataFrame({'Year': years})
    df_count = df_years.value_counts().reset_index()
    df_count.columns = ['Year', 'Count']
    df_count = df_count.sort_values('Year')
    
    fig1 = px.bar(df_count, x='Year', y='Count',
                  title='Number of Collections per Year',
                  color='Count',
                  color_continuous_scale='purples')
    
    # Chart 2: Top 5 Designer Nationalities
    designers = pd.read_sql('Designers', con=engine)
    top_nationalities = designers['nationality'].value_counts().head(5).reset_index()
    top_nationalities.columns = ['Nationality', 'Count']
    
    fig2 = px.bar(top_nationalities, x='Nationality', y='Count',
                  title='Top 5 Designer Nationalities',
                  color='Nationality',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    
    # Chart 3: Top 5 Contributors by Contribution Percentage
    designers_collections = pd.read_sql('Designers_collections', con=engine)
    contributors_sum = (
        designers_collections.groupby('designer_id')['contribution_percentage']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    
    designer_names = designers[['designer_id', 'name']]
    contributors_sum = contributors_sum.merge(designer_names, on='designer_id')
    
    fig3 = px.pie(contributors_sum, names='name', values='contribution_percentage',
                  title='Top 5 Contributors (by % Contribution)',
                  color_discrete_sequence=px.colors.sequential.Purples)
    
    # Chart 4: Fashion Shows Over Time (scatter)
    fashion_shows = pd.read_sql('Fashion_show', con=engine)
    fashion_shows['date'] = pd.to_datetime(fashion_shows['date'], errors='coerce')
    fashion_shows = fashion_shows.dropna(subset=['date']).sort_values('date')

    fig4 = px.scatter(fashion_shows, x='date', y='show_name',
                      title='Fashion Shows Over Time',
                      labels={'date': 'Date', 'show_name': 'Show Name'},
                      hover_name='venue',
                      color_discrete_sequence=['blue'])
    
    # Layout adjustments common to all charts
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(
            margin=dict(l=50, r=50, t=80, b=50),
            height=400,
            showlegend=False
        )
    
    # Convert all charts to HTML snippets
    plot_div1 = fig1.to_html(full_html=False, include_plotlyjs='cdn', div_id="plot1")
    plot_div2 = fig2.to_html(full_html=False, include_plotlyjs=False, div_id="plot2")
    plot_div3 = fig3.to_html(full_html=False, include_plotlyjs=False, div_id="plot3")
    plot_div4 = fig4.to_html(full_html=False, include_plotlyjs=False, div_id="plot4")

    return render_template("plotly.html", 
                           plot_div1=plot_div1,
                           plot_div2=plot_div2,
                           plot_div3=plot_div3,
                           plot_div4=plot_div4,
                           ulogin=session.get("user"))

