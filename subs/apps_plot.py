import io
import matplotlib.pyplot as plt
from flask import Response
from classes.collections import Collections
from flask import session

def apps_plot():
    # Extrair os anos de lançamento das coleções
    anos = [c.release_year for c in Collections.obj.values() if c.release_year]

    # Contar quantas coleções existem por ano
    from collections import Counter
    contagem = Counter(anos)

    # Ordenar os anos
    anos_ordenados = sorted(contagem.keys())
    quantidades = [contagem[ano] for ano in anos_ordenados]

    # Criar o gráfico de barras
    plt.figure(figsize=(8,5))
    plt.bar(anos_ordenados, quantidades, color='purple')
    plt.title('Número de coleções por ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de coleções')
    plt.grid(axis='y')

    # Salvar o gráfico no buffer em PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return Response(buf.getvalue(), mimetype='image/png')
