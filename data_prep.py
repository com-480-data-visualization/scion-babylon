import pandas as pd
import gender_guesser.detector as gender

"""
Code to generate one main gendered database of authors
Method:
- Use international bestsellers to get first entries
-
"""


# load datasets
best_books = pd.read_csv("books_1.Best_Books_Ever.csv")
best_books['author'] = best_books['author'].str.strip('"').str.replace(r'\(Goodreads Author\)', '', regex=True).str.strip()

## Strip other roles outside from author
best_books['author'] = best_books['author'].str.replace(r',\s*[^,]+\([^)]+\)', '', regex=True).str.strip().str.strip(',').str.strip()
international_bestsellers = pd.read_csv("international_bestsellers.csv")

rest = best_books[~best_books['title'].isin(international_bestsellers['title'])]
rest = rest.drop_duplicates(subset=["title"])
df = rest[["title","author", "rating", "genres", "language"]].copy()

merged = pd.merge(best_books, international_bestsellers[['title', 'gender']], on='title', how='inner')
merged = merged[["title","author", "rating", "genres", "language", "gender"]]
## apply gender detector
# possible outputs unknown, andy, male, female, mostly_male, or mostly_female

d = gender.Detector()
df['gender']= df["author"].apply(lambda x: d.get_gender(x.split()[0]))
df.drop(df.loc[df['gender']=="unknown"].index, inplace=True)

df_known = df[df['gender'].isin(["male", "female"])]
df_known['gender'] = df_known['gender'].apply(lambda g: 'w' if g == "female" else 'm')
df_known = df_known.drop_duplicates(subset=["title"])
df_merged = pd.concat([df_known, merged])
df_merged = df_merged.drop_duplicates(subset=["title"])
df_merged.to_csv("genders_ratings.csv", index=False)

international_bestsellers = international_bestsellers[["title","author", "gender"]] #TODO figure out language/nazionality
df_merged_gender = pd.concat([df_merged[["title","author", "gender"]], international_bestsellers])
df_merged_gender.to_csv("genders.csv", index=False)
