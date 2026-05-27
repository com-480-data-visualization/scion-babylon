import pandas as pd
import os

"""
Generate bookshelf.csv for the visualization
Columns: title, author, rating, genres, language, gender, description

Uses existing gender data from genders_ratings.csv and adds description from best_books
"""

cwd = os.getcwd().split("/")[-1]
if cwd != "data":
    raise ValueError('Please run this script from inside the data directory')

# Load datasets
best_books = pd.read_csv("datasets/books_1.Best_Books_Ever.csv")
genders_ratings = pd.read_csv("datasets/genders_ratings.csv")

# Keep only needed columns from best_books
best_books_clean = best_books[["title", "description", "publishDate"]].copy()

# Merge with gender data
df = pd.merge(genders_ratings[["title", "author", "rating", "genres", "language", "gender"]],
              best_books_clean,
              on="title",
              how="left")

# Select required columns in order
df = df[["title", "author", "rating", "genres", "language", "gender", "description", "publishDate"]]

# Remove rows without description
df = df.dropna(subset=["description"])

# Remove duplicates
df = df.drop_duplicates(subset=["title"])

# Save to website static folder
output_path = "../website/static/data/bookshelf.csv"
df.to_csv(output_path, index=False)

print(f"Generated {len(df)} books")
print(f"Saved to {output_path}")
print(f"Female authors: {len(df[df['gender'] == 'w'])}")
print(f"Male authors: {len(df[df['gender'] == 'm'])}")
