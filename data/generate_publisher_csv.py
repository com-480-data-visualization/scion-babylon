import pandas as pd
import os
import re
import ast
from collections import Counter

"""
Generate a publisher-level CSV with counts of male/female authors per publisher.

Output columns: publisher, num_male, num_female

Notes:
- Counts are computed by counting occurrences of 'm' and 'w' in the `gender` field
  (e.g. 'm;m' counts as 2 males). Missing publishers are set to 'Unknown'.
"""

cwd = os.getcwd().split("/")[-1]
if cwd != "data":
    raise ValueError('Please run this script from inside the data directory')

# Load datasets
best_books = pd.read_csv("datasets/books_1.Best_Books_Ever.csv")
genders_ratings = pd.read_csv("datasets/genders_ratings.csv")

# Keep only needed columns from best_books
best_books_clean = best_books[["title", "publisher", "publishDate"]].copy()

# Merge with gender data
df = pd.merge(
    genders_ratings[["title", "author", "rating", "genres", "language", "gender"]],
    best_books_clean,
    on="title",
    how="left",
)

# Select required columns in order and drop duplicate titles
df = df[["title", "author", "rating", "gender", "genres", "publisher", "publishDate"]]
df = df.drop_duplicates(subset=["title"])

# Normalize publisher values and gender field
df = df.dropna(subset=["publisher"])
df["gender"] = df["gender"].fillna("").astype(str)

# Parse genres column
def parse_genres(s):
    if pd.isna(s) or s == "":
        return []
    try:
        res = ast.literal_eval(s)
        if "Fiction" in res: 
            res.remove("Fiction")
        return res
    except:
        return []

df["genres_list"] = df["genres"].apply(parse_genres)

# Count male/female occurrences in the gender string (simple, robust for 'm', 'w', 'm;m', 'w;w')
def count_genders(s: str):
    s_low = s.lower()
    # count occurrences of single-letter tokens 'm' and 'w'
    num_m = s_low.count('m')
    num_w = s_low.count('w')
    return num_m, num_w

counts = df["gender"].apply(lambda s: pd.Series(dict(zip(["male", "female"], count_genders(s)))))
df["male_count"] = counts["male"]
df["female_count"] = counts["female"]

# Aggregate per publisher
def get_top_genres(group_genres_list):
    """Extract top 3 genres from a group of genre lists"""
    all_genres = []
    for genres_list in group_genres_list:
        all_genres.extend(genres_list)

    if not all_genres:
        return ""

    counter = Counter(all_genres)
    top_3 = counter.most_common(3)
    return ", ".join([genre for genre, count in top_3])

agg = (
    df.groupby("publisher", dropna=False)
    .agg(
        num_male=("male_count", "sum"),
        num_female=("female_count", "sum"),
        top_genres=("genres_list", get_top_genres)
    )
    .reset_index()
)

# Optional: sort by total authors (descending)
agg["total"] = agg["num_male"] + agg["num_female"]
agg = agg.sort_values("total", ascending=False).drop(columns=["total"])

# Save aggregated output
output_path = "../website/static/data/publisher_gender_counts.csv"
agg.to_csv(output_path, index=False)

print(f"Generated {len(agg)} publishers")
print(f"Saved publisher gender counts to {output_path}")