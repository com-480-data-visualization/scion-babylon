import pandas as pd
import gender_guesser.detector as gender
import os

cwd = os.getcwd().split("/")[-1]
if cwd != "data":
    raise ValueError('Please run this script from inside the data directory')

#load dataset
df_test = pd.read_csv("datasets/test.csv")
defined_genres = {"Nonfiction", "Science Fiction", "Fantasy", "Thriller", "Classics", "Romance", "Philosophy", "Horror", "Childrens", "Young Adult", "Poetry", "Feminism", "Drama","Young Adult", "Literary Fiction"}


## create gender-genres dataset
def find_genre(series):
    list_genres = series.strip("[]").replace("'", "").split(",")
    print(f"list_genres : {list_genres}")
    for i,s in enumerate(list_genres):
        print(f"{i}: {s}")
        s = s.strip()
        if s in defined_genres:
            return s
    return list_genres[0] if len(list_genres) > 0 else None

df_test["genre"] = df_test["genres_list"].apply(find_genre)

df_unknown = df_test[~df_test["genre"].isin(defined_genres)]
df_unknown.to_csv("datasets/test_unknown_genres.csv")
print(f"df_unknown: {len(df_unknown)}")
df_test = df_test[df_test["genre"].isin(defined_genres)]
print(f"df_known: {len(df_test)}")

df_test = df_test[["gender", "genre"]]
df_test["gender"] = df_test["gender"].apply(lambda s: "w;m" if s == "m;w" else s)
df_test.to_csv("datasets/test_genders_genres.csv", index=False)
