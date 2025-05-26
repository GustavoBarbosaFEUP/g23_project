import io
import base64
import matplotlib.pyplot as plt
from flask import render_template
from classes.collections import Collections

def apps_plot():
    # Extrair os anos de lançamento das coleções (filtrando valores válidos)
    anos = [c.release_year for c in Collections.obj.values() if c.release_year]

    from collections import Counter
    contagem = Counter(anos)

    # Ordenar os anos
    anos_ordenados = sorted(contagem.keys())
    quantidades = [contagem[ano] for ano in anos_ordenados]

    # Criar gráfico de barras
    plt.figure(figsize=(8,5))
    plt.bar(anos_ordenados, quantidades, color='purple')
    plt.title('Número de coleções por ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de coleções')
    plt.grid(axis='y')
    plt.tight_layout()

    # Salvar gráfico em PNG no buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Codificar imagem para base64 (para passar ao template HTML)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Renderizar template passando a imagem codificada
    return render_template('plot.html', plot_url=image_base64)
