import pandas as pd
import re

international_bestsellers = pd.read_csv("datasets/international_bestsellers.csv")
international_bestsellers = international_bestsellers.drop_duplicates(subset=["title"])
all_countries = pd.read_csv("datasets/all.csv")
all_countries = all_countries[["name", "country-code"]]

nationalities = international_bestsellers[["author", "nationality"]]
aliases = {
    "Vietnam": "Viet Nam",
    "Turkey": "Türkiye",
    "South Korea": "Korea, Republic of",
    "Morroco": "Morocco",
    "Ivory Coast": "Côte d'Ivoire",
    "Czech Republic": "Czechia",
    "Scotland": "United Kingdom of Great Britain and Northern Ireland",
    "Algiers": "Algeria"
}


def find_match(nationality, country_names):
    nationality_lower = nationality.lower()
    for name in country_names:
        if nationality_lower in name.lower() or name.lower() in nationality_lower:
            return name
    if nationality in aliases:
        return aliases[nationality]
    return None

nationalities["nationality"] = nationalities["nationality"].apply(lambda n: re.findall(r"[\w'\s]+", str(n))).explode("nationality")
nationalities["nationality"] = nationalities["nationality"].str.lstrip()
nationalities = nationalities.groupby(['nationality']).size().reset_index(name='counts')

all_names = all_countries["name"].tolist()

nationalities["matched_name"] = nationalities["nationality"].apply(
    lambda n: find_match(n, all_names)
)

merged = pd.merge(nationalities, all_countries, left_on='matched_name', right_on='name', how='left')

merged = merged.rename(columns={"country-code": "ID"})

def exceptions(series):
    if series.iloc[0] == "Scotland":
        return "United Kingdom"
    return series.iloc[0]

merged_agg = (merged
    .groupby("ID", dropna=False)
    .agg(
        nationality = ("nationality",exceptions),
        counts=("counts", "sum")
    )
    .reset_index()
)
merged_agg["ID"] = merged_agg["ID"].dropna()
merged_agg = merged_agg[merged_agg["ID"].notna()]
merged_agg["ID"] = merged_agg["ID"].astype(int)
merged_agg.to_csv("datasets/nationalities.csv", index=False)
