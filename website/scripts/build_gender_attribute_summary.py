from pathlib import Path
import csv
import re

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "datasets"
OUTPUT = Path(__file__).resolve().parents[1] / "static" / "data" / "gender_attribute_summary.csv"


def classify_gender(value):
    text = str(value).strip().lower()
    if not text or text == "nan":
        return "unknown"

    parts = [part.strip() for part in re.split(r"[;,]", text) if part.strip()]
    if not parts:
        return "unknown"

    mapped = []
    for part in parts:
        if part in {"m", "male", "mostly_male"}:
            mapped.append("m")
        elif part in {"w", "f", "female", "mostly_female"}:
            mapped.append("w")
        else:
            mapped.append("unknown")

    known = [part for part in mapped if part in {"m", "w"}]
    if not known or len(known) != len(mapped):
        return "unknown"
    if all(part == "m" for part in known):
        return "men"
    if all(part == "w" for part in known):
        return "women"
    return "mixed"


def rows_from_grouped(frame, attribute_type, attribute_column, count_column=None):
    if count_column:
        grouped = frame.groupby([attribute_column, "gender_class"], as_index=False)[count_column].sum()
    else:
        grouped = (
            frame.groupby([attribute_column, "gender_class"], as_index=False)
            .size()
            .rename(columns={"size": "count"})
        )
        count_column = "count"

    pivot = grouped.pivot_table(
        index=attribute_column,
        columns="gender_class",
        values=count_column,
        aggfunc="sum",
        fill_value=0,
    )
    for column in ["men", "women", "mixed", "unknown"]:
        if column not in pivot.columns:
            pivot[column] = 0

    rows = []
    for _, row in pivot.reset_index().iterrows():
        men = int(row["men"])
        women = int(row["women"])
        mixed = int(row["mixed"])
        unknown = int(row["unknown"])
        total = men + women + mixed + unknown
        gendered_total = men + women
        pct_women = women / gendered_total if gendered_total else 0
        pct_men = men / gendered_total if gendered_total else 0
        disparity = pct_women - pct_men if gendered_total else 0

        rows.append(
            {
                "attribute_type": attribute_type,
                "attribute": row[attribute_column],
                "men": men,
                "women": women,
                "mixed": mixed,
                "unknown": unknown,
                "total": total,
                "gendered_total": gendered_total,
                "pct_women": round(pct_women, 4),
                "pct_men": round(pct_men, 4),
                "disparity": round(disparity, 4),
            }
        )
    return rows


def build_rows():
    genres = pd.read_csv(DATA_DIR / "genders_genres.csv")
    genres["gender_class"] = genres["gender"].apply(classify_gender)
    genre_rows = rows_from_grouped(genres, "genre", "genres", "count")

    # Country aggregation is based on author nationality, not publication country.
    origins = pd.read_csv(DATA_DIR / "international_bestsellers.csv")
    origins = origins.drop_duplicates(subset=["title"]).copy()
    origins["gender_class"] = origins["gender"].apply(classify_gender)
    origins["nationality"] = origins["nationality"].fillna("Unknown").astype(str)
    origins["nationality"] = origins["nationality"].apply(
        lambda value: [item.strip() for item in re.split(r"[,;/]", value) if item.strip()]
    )
    origins = origins.explode("nationality")
    origins = origins[origins["nationality"].ne("Unknown")]
    origin_rows = rows_from_grouped(origins, "origin", "nationality")

    rows = genre_rows + origin_rows
    rows.sort(key=lambda row: (row["attribute_type"], -row["total"], row["attribute"]))
    return rows


def main():
    fieldnames = [
        "attribute_type",
        "attribute",
        "men",
        "women",
        "mixed",
        "unknown",
        "total",
        "gendered_total",
        "pct_women",
        "pct_men",
        "disparity",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(build_rows())
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
