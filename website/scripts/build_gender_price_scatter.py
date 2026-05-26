from pathlib import Path
import re

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "datasets"
OUTPUT = Path(__file__).resolve().parents[1] / "static" / "data" / "gender_price_scatter.csv"
GENRES = {
    "Nonfiction",
    "Science Fiction",
    "Fantasy",
    "Thriller",
    "Classics",
    "Romance",
    "Philosophy",
    "Horror",
    "Childrens",
    "Young Adult",
    "Poetry",
}


def find_genre(value):
    items = [item.strip().strip("'") for item in str(value).strip("[]").split(",")]
    return next((item for item in items if item in GENRES), None)


def gender_group(value):
    parts = [part.strip() for part in re.split(r"[;,]", str(value)) if part.strip()]
    if parts and all(part == "m" for part in parts):
        return "Male authors"
    if parts and any(part == "w" for part in parts) and all(part in {"m", "w"} for part in parts):
        return "Non-male authors"
    return None


def aggregate(frame, attribute_type, attribute_column):
    summary = (
        frame.groupby([attribute_column, "gender_group"], as_index=False)
        .agg(
            average_price=("price", "mean"),
            average_rating=("rating", "mean"),
            books=("title", "count"),
        )
        .rename(columns={attribute_column: "attribute"})
    )
    summary.insert(0, "attribute_type", attribute_type)
    return summary


def main():
    books = pd.read_csv(DATA_DIR / "books_1.Best_Books_Ever.csv").drop_duplicates(subset=["title"])
    gendered = pd.read_csv(DATA_DIR / "genders_ratings.csv").drop_duplicates(subset=["title"])

    genres = gendered.merge(books[["title", "price"]], on="title", how="left")
    genres["genre"] = genres["genres"].apply(find_genre)
    genres["gender_group"] = genres["gender"].apply(gender_group)
    genres["price"] = pd.to_numeric(genres["price"], errors="coerce")
    genres["rating"] = pd.to_numeric(genres["rating"], errors="coerce")
    genres = genres.dropna(subset=["genre", "gender_group", "price", "rating"])

    # Nationality is the author's nationality from the bestseller data, not publication country.
    nationality = pd.read_csv(DATA_DIR / "international_bestsellers.csv").drop_duplicates(subset=["title"])
    nationality = nationality.merge(books[["title", "price", "rating"]], on="title", how="inner")
    nationality["gender_group"] = nationality["gender"].apply(gender_group)
    nationality["nationality"] = nationality["nationality"].fillna("Unknown").astype(str).apply(
        lambda value: [item.strip() for item in re.split(r"[,;/]", value) if item.strip()]
    )
    nationality = nationality.explode("nationality")
    nationality["price"] = pd.to_numeric(nationality["price"], errors="coerce")
    nationality["rating"] = pd.to_numeric(nationality["rating"], errors="coerce")
    nationality = nationality.dropna(subset=["nationality", "gender_group", "price", "rating"])
    nationality = nationality[nationality["nationality"].ne("Unknown")]

    summary = pd.concat(
        [
            aggregate(genres, "genre", "genre"),
            aggregate(nationality, "nationality", "nationality"),
        ],
        ignore_index=True,
    ).sort_values(["attribute_type", "attribute", "gender_group"])
    summary["average_price"] = summary["average_price"].round(2)
    summary["average_rating"] = summary["average_rating"].round(3)
    summary.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT} from {len(genres)} genre books and {len(nationality)} nationality-linked books")


if __name__ == "__main__":
    main()
