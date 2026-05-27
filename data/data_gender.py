import pandas as pd
import gender_guesser.detector as gender
import os

cwd = os.getcwd().split("/")[-1]
if cwd != "data":
    raise ValueError('Please run this script from inside the data directory')

# load datasets
best_books = pd.read_csv("datasets/books_1.Best_Books_Ever.csv")
best_books['author'] = best_books['author'].str.strip('"').str.replace(r'\(Goodreads Author\)', '', regex=True).str.strip()

# Strip other roles outside from author
best_books['author'] = best_books['author'].str.replace(r',\s*[^,]+\([^)]+\)', '', regex=True).str.strip().str.strip(',').str.strip()
international_bestsellers = pd.read_csv("datasets/international_bestsellers.csv")
international_bestsellers = international_bestsellers.drop_duplicates(subset=["title"])

rest = best_books[~best_books['title'].isin(international_bestsellers['title'])]
rest = rest.drop_duplicates(subset=["title"])
df = rest[["title","author", "rating", "genres", "language"]].copy()


## Apply gender detector
# possible outputs unknown, andy, male, female, mostly_male, or mostly_female
d = gender.Detector()
def guess_gender(authors: str):
    split_authors = authors.split(",")

    if (len(split_authors) == 1):
        name = split_authors[0].split()[0]
        return 'w' if d.get_gender(name) == "female" else 'm'

    # more than one name
    final_gender = ""
    for author in split_authors:
        name = author.split()[0]
        if len(final_gender) > 0:
            final_gender += ";"
        gender = d.get_gender(name)
        match gender:
            case "female":
                final_gender += "w"
            case "male":
                final_gender += "m"
            case _:
                final_gender += gender
    return final_gender


df['gender']= df["author"].apply(lambda x: guess_gender(x))

df_known = df[df['gender'].isin(["m", "w", "m;m", "w;m", "m;w", "w;w"])]
df_known = df_known.drop_duplicates(subset=["title"])

merged = pd.merge(best_books, international_bestsellers[['title', 'gender']], on='title', how='inner')
merged["gender"] = merged["gender"].apply(lambda g: str(g).replace(" ", "").replace(",", ";"))

merged = merged[["title","author", "rating", "genres", "language", "gender"]]
df_merged = pd.concat([df_known, merged ])
df_merged = df_merged.drop_duplicates(subset=["title"])
defined_genres = {"Nonfiction", "Science Fiction", "Fantasy", "Thriller", "Classics", "Romance", "Philosophy", "Horror", "Childrens", "Young Adult", "Poetry"}


## create gender-genres dataset
def find_genre(series):
    list_genres = series.strip("[]").replace("'", "").split(",")
    for s in list_genres:
        s = s.strip()
        if s in defined_genres:
            return s
    return list_genres[0] if len(list_genres) > 0 else None

df_merged["genres"] = df_merged["genres"].apply(find_genre)

df_unknown = df_merged[~df_merged["genres"].isin(defined_genres)]
df_unknown.to_csv("datasets/unkown_genres.csv")
print(f"df_unknown: {len(df_unknown)}")
df_merged = df_merged[df_merged["genres"].isin(defined_genres)]

df_merged = df_merged[["gender", "genres"]]
df_merged["count"] = df_merged.groupby(["gender", "genres"])["gender"].transform("count")

df_merged = df_merged.drop_duplicates(subset=["gender", "genres"]).sort_values(by=["genres"])

print(f"gender with ratings: {len(df_merged)}")
df_merged.to_csv("datasets/genders_genres.csv", index=False)
