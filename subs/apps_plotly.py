from flask import render_template
import pandas as pd
import plotly.express as px
import os

def apps_plotly():
    # Caminho correto e simples para o CSV atualizado
    csv_path = os.path.join('data', 'G23_Fashion.csv')

    try:
        df = pd.read_csv(csv_path)

        # Exemplo de gráfico simples com dados reais
        if 'release_year' in df.columns:
            df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
            df_grouped = df.groupby('release_year').size().reset_index(name='Quantidade de Coleções')
            fig = px.bar(df_grouped, x='release_year', y='Quantidade de Coleções', title='Número de Coleções por Ano')
        else:
            fig = px.bar(title="Erro: Coluna 'release_year' não encontrada no CSV")

        graph_html = fig.to_html(full_html=False)
        return render_template('plot.html', graph_html=graph_html)

    except Exception as e:
        # Mostrar erro no navegador para debug
        return f"<h1>Erro ao carregar gráfico:</h1><p>{e}</p>"
