from flask import render_template
import pandas as pd
import plotly.express as px

def apps_plotly():
    # Caminho para o CSV (verifica o nome e caminho correto)
    df = pd.read_csv('data/G23_Fashion – Designers  Collections with Fashion Shows_merged (1).csv')

    # Exemplo: Gráfico de contagem de designers por nacionalidade
    fig = px.histogram(df, x='Designer Nationality', title='Designers por Nacionalidade')
    graph_html = fig.to_html(full_html=False)

    return render_template('plot.html', graph_html=graph_html)
