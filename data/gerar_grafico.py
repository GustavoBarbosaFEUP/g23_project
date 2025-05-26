import pandas as pd
import matplotlib.pyplot as plt

# Ler o CSV (ajuste o nome exato se necessário)
df = pd.read_csv("data/G23_Fashion – Designers  Collections with Fashion Shows_merged.csv")

# Contar coleções por estação
season_counts = df['season'].value_counts()

# Ordenar manualmente
ordered_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
season_counts = season_counts.reindex(ordered_seasons, fill_value=0)

# Criar o gráfico
plt.figure(figsize=(6, 4))
season_counts.plot(kind='bar', color='lightblue', edgecolor='black')
plt.title("Número de coleções por estação")
plt.xlabel("Estação")
plt.ylabel("Número de coleções")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Salvar o gráfico como imagem
plt.savefig("grafico_estacoes.png")
print("✅ Gráfico salvo como grafico_estacoes.png")
