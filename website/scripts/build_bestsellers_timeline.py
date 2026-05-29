from pathlib import Path
import re

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "datasets"
OUTPUT = Path(__file__).resolve().parents[1] / "static" / "data" / "bestsellers_timeline.csv"
ALL_ORIGINS = "All origins"


def classify_gender(value):
    parts = [
        part.strip().lower()
        for part in re.split(r"[;,]", str(value))
        if part.strip() and part.strip().lower() != "nan"
    ]
    if not parts:
        return "unknown"
    if all(part in {"m", "male", "mostly_male"} for part in parts):
        return "men"
    if all(part in {"w", "f", "female", "mostly_female"} for part in parts):
        return "women"
    if all(part in {"m", "male", "mostly_male", "w", "f", "female", "mostly_female"} for part in parts):
        return "mixed"
    return "unknown"


def split_origins(value):
    origins = [item.strip() for item in re.split(r"[,;/]", str(value)) if item.strip()]
    return origins or ["Unknown"]


def publication_year(row):
    for column in ["firstPublishDate", "publishDate"]:
        text = str(row.get(column, "")).strip()
        if not text or text == "nan":
            continue
        year_match = re.search(r"(1[5-9]\d{2}|20\d{2})", text)
        if year_match:
            return int(year_match.group(1))
        short_year_match = re.search(r"(?:^|/)(\d{2})$", text)
        if short_year_match:
            year = int(short_year_match.group(1))
            return 2000 + year if year <= 26 else 1900 + year
    return None


def representative_title(frame):
    title_rows = (
        frame.groupby(["title", "author", "nationality"], dropna=False, as_index=False)
        .agg(
            appearances=("entry_id", "count"),
            best_rank=("rank", "min"),
            rating=("rating", "mean"),
        )
        .sort_values(["rating", "appearances", "best_rank", "title"], ascending=[False, False, True, True])
    )
    return title_rows.iloc[0]


def summarize(group):
    featured = representative_title(group)
    return pd.Series(
        {
            "appearances": len(group),
            "titles": group["title"].nunique(),
            "number_one_appearances": int((group["rank"] == 1).sum()),
            "markets": group["country"].nunique(),
            "average_rating": round(group["rating"].mean(), 2),
            "featured_title": featured["title"] if featured is not None else "",
            "featured_author": featured["author"] if featured is not None else "",
            "featured_origin": featured["nationality"] if featured is not None else "",
            "featured_rating": round(float(featured["rating"]), 2) if featured is not None else "",
            "featured_appearances": int(featured["appearances"]) if featured is not None else 0,
            "featured_best_rank": int(featured["best_rank"]) if featured is not None else 0,
        }
    )


def main():
    books = pd.read_csv(DATA_DIR / "international_bestsellers.csv")
    latest_ranking_year = pd.to_datetime(books["date"]).dt.year.max()
    ratings = pd.read_csv(DATA_DIR / "books_1.Best_Books_Ever.csv")[
        ["title", "rating", "publishDate", "firstPublishDate"]
    ]
    ratings = ratings.drop_duplicates(subset=["title"])
    ratings["rating"] = pd.to_numeric(ratings["rating"], errors="coerce")
    ratings["year"] = ratings.apply(publication_year, axis=1)
    books = books.merge(ratings, on="title", how="left")
    books["gender_class"] = books["gender"].apply(classify_gender)
    books["nationality"] = books["nationality"].fillna("Unknown")
    books = books.dropna(subset=["rating", "year"])
    books["year"] = books["year"].astype(int)
    books = books[books["year"].le(latest_ranking_year)]

    all_origins = books.copy()
    all_origins["origin"] = ALL_ORIGINS

    by_origin = books.copy()
    by_origin["origin"] = by_origin["nationality"].apply(split_origins)
    by_origin = by_origin.explode("origin")
    by_origin = by_origin[by_origin["origin"].ne("Unknown")]
    by_origin = by_origin.drop_duplicates(subset=["entry_id", "origin"])

    timeline = pd.concat([all_origins, by_origin], ignore_index=True)
    summary = (
        timeline.groupby(["origin", "year", "gender_class"], sort=False)
        .apply(summarize)
        .reset_index()
        .sort_values(["origin", "year", "gender_class"])
    )
    summary.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT} with {len(summary)} yearly gender/origin summaries")


if __name__ == "__main__":
    main()
