import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o ficheiro CSV
# Certifique-se de que esse CSV também esteja no repositório
csv_path = "data/G23_Fashion – Designers  Collections with Fashion Shows_merged.csv"

# Ler os dados
df = pd.read_csv(csv_path)

# Contar número de coleções por estação
season_counts = df['season'].value_counts()

# Garantir ordem correta
ordered_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
season_counts = season_counts.reindex(ordered_seasons, fill_value=0)

# Criar gráfico de barras
season_counts.plot(kind='bar', color='lightblue', edgecolor='black')
plt.title("Número de coleções por estação")
plt.xlabel("Estação")
plt.ylabel("Número de coleções")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrar gráfico
plt.show()
