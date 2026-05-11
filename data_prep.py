import pandas as pd
import gender_guesser.detector as gender

"""
Code to generate 3 databases of authors: gendered with ratings, only genders and undefined gender
Method:
- Remove titles that are in international bestsellers database
- Use gender guesser to get gender of books in best books database
- Use international bestseller to add the gender of known books
"""


# load datasets
best_books = pd.read_csv("books_1.Best_Books_Ever.csv")
best_books['author'] = best_books['author'].str.strip('"').str.replace(r'\(Goodreads Author\)', '', regex=True).str.strip()

# Strip other roles outside from author
best_books['author'] = best_books['author'].str.replace(r',\s*[^,]+\([^)]+\)', '', regex=True).str.strip().str.strip(',').str.strip()
international_bestsellers = pd.read_csv("international_bestsellers.csv")

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

# Output unclassified genders
df_undefined = df[~df['gender'].isin(["m", "w", "m;m", "w;m", "m;w", "w;w"])]
df_undefined.to_csv("gender_undefined.csv", index=False)
print(f"undefined: {len(df_undefined)}")

df_known = df[df['gender'].isin(["m", "w", "m;m", "w;m", "m;w", "w;w"])]
df_known = df_known.drop_duplicates(subset=["title"])

merged = pd.merge(best_books, international_bestsellers[['title', 'gender']], on='title', how='inner')
merged = merged[["title","author", "rating", "genres", "language", "gender"]]
df_merged = pd.concat([df_known, merged])
df_merged = df_merged.drop_duplicates(subset=["title"])
df_merged.to_csv("genders_ratings.csv", index=False)
print(f"gender with ratings: {len(df_merged)}")

international_bestsellers = international_bestsellers[["title","author", "gender"]]
df_merged_gender = pd.concat([df_merged[["title","author", "gender"]], international_bestsellers])
df_merged_gender = df_merged_gender.drop_duplicates(subset=["title"])
df_merged_gender.to_csv("genders.csv", index=False)
print(f"gender: {len(df_merged_gender)}")
