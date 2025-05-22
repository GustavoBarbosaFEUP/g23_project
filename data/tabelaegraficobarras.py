# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
pip install pandas
# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
df = pd.read_csv("G23_Fashion – Designers  Collections with Fashion Shows_merged.csv")
df.head()

# %%
season_counts = df['season'].value_counts()
ordered_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
season_counts = season_counts.reindex(ordered_seasons, fill_value=0)

# %%
season_counts.plot(kind='bar', color='lightblue', edgecolor='black')
plt.title("Número de coleções por estação")
plt.xlabel("Estação")
plt.ylabel("Número de coleções")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# %%

