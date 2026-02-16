import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs('outputs', exist_ok=True)
import seaborn as sns

df = pd.read_csv("All_Diets.csv")

print(df.head())
print(df.info())

cols_to_fill = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[cols_to_fill] = df[cols_to_fill].fillna(df[cols_to_fill].mean())

avg_macros = df.groupby('Diet_type')[cols_to_fill].mean()
print(avg_macros)

top_protein = (
    df.sort_values('Protein(g)', ascending=False)
    .groupby('Diet_type')
    .head(5)
)
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print("Diet with highest average protein: ", highest_protein_diet)

common_cuisines = (
    df.groupby('Diet_type')['Cuisine_type']
    .agg(lambda x: x.value_counts().idxmax())
)
print(common_cuisines)

df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0, 1e-6)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0, 1e-6)

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title("Average Protein by Diet Type")
plt.xticks(rotation=45)
plt.ylabel("Protein (g)")
plt.tight_layout()
plt.tight_layout()
plt.savefig(f'outputs/figure_{plt.gcf().number}.png', dpi=200)
plt.show()

plt.figure(figsize=(10, 6))
sns.heatmap(avg_macros, annot=True, cmap="coolwarm")
plt.title("Macronutrient Distribution by Diet Type")
plt.tight_layout()
plt.savefig(f'outputs/figure_{plt.gcf().number}.png', dpi=200)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=top_protein,
    x='Protein(g)',
    y='Carbs(g)',
    hue='Cuisine_type'
)
plt.title("Top Protein-Rich Recipes by Cuisine")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.tight_layout()
plt.savefig(f'outputs/figure_{plt.gcf().number}.png', dpi=200)
plt.show()
