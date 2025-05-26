import pandas as pd
import plotly.graph_objs as go
from flask import render_template
from classes.collections import Collections

def apps_plotly():
    # Extrair os anos de lançamento das coleções (filtrando valores válidos)
    anos = [c.release_year.year for c in Collections.obj.values() if c.release_year]

    from collections import Counter
    contagem = Counter(anos)

    # Ordenar os anos
    anos_ordenados = sorted(contagem.keys())
    quantidades = [contagem[ano] for ano in anos_ordenados]

    # Criar gráfico de barras Plotly
    fig = go.Figure(data=[go.Bar(
        x=anos_ordenados,
        y=quantidades,
        marker_color='purple'
    )])

    fig.update_layout(
        title='Número de coleções por ano',
        xaxis_title='Ano',
        yaxis_title='Quantidade de coleções'
    )

    # Gerar HTML + JS do gráfico Plotly para inserir no template
    plot_div = fig.to_html(full_html=False)

    # Renderizar template passando o gráfico embutido
    return render_template('plotly.html', plot_div=plot_div)
