import pandas as pd
import re

international_bestsellers = pd.read_csv("datasets/international_bestsellers.csv")
international_bestsellers = international_bestsellers.drop_duplicates(subset=["title"])

all_countries = pd.read_csv("datasets/all.csv")
population = pd.read_csv("datasets/population.csv")
all_countries = all_countries.merge(population, left_on="alpha-3", right_on="Country Code")

year_cols = [str(y) for y in range(1960, 2025)]
all_countries = all_countries[["name", "country-code", "alpha-2"] + year_cols]

# Melt population into long format: one row per (country, year)
pop_long = all_countries.melt(
    id_vars=["name", "country-code", "alpha-2"],
    value_vars=year_cols,
    var_name="year",
    value_name="population"
)
pop_long["year"] = pop_long["year"].astype(int)
pop_long["population"] = pd.to_numeric(pop_long["population"], errors="coerce")

aliases = {
    "Vietnam": "Viet Nam",
    "Turkey": "Türkiye",
    "South Korea": "Korea, Republic of",
    "Morroco": "Morocco",
    "Ivory Coast": "Côte d'Ivoire",
    "Czech Republic": "Czechia",
    "Scotland": "United Kingdom of Great Britain and Northern Ireland",
    "Algiers": "Algeria",
    "Taiwan": "Taiwan, Province of China"
}

def find_match(nationality, country_names):
    nationality_lower = nationality.lower().strip()
    country_names.sort(key = len, reverse = True)
    for name in country_names:
        if nationality_lower in name.lower() or name.lower() in nationality_lower:
            return name
    if nationality.strip() in aliases:
        return aliases[nationality.strip()]
    return None

nationalities = international_bestsellers[["author", "nationality", "date"]].copy()
nationalities["nationality"] = (
    nationalities["nationality"]
    .apply(lambda n: re.findall(r"[\w'\s]+", str(n)))
)
nationalities = nationalities.explode("nationality")
nationalities["nationality"] = nationalities["nationality"].str.strip()
nationalities = nationalities[nationalities["nationality"].str.len() > 0]
nationalities["year"] = pd.to_datetime(nationalities["date"], errors="coerce").dt.year

grouped = (
    nationalities
    .groupby(["nationality", "year"])
    .size()
    .reset_index(name="counts")
)

all_names = all_countries["name"].tolist()
grouped["matched_name"] = grouped["nationality"].apply(
    lambda n: find_match(n, all_names)
)

country_meta = all_countries[["name", "country-code", "alpha-2"]].copy()
merged = pd.merge(
    grouped,
    country_meta,
    left_on="matched_name",
    right_on="name",
    how="left"
)
merged = merged.rename(columns={"country-code": "ID", "alpha-2":"alpha2"})

def exceptions(series):
    if series.iloc[0] == "Scotland":
        return "United Kingdom"
    return series.iloc[0]

merged_agg = (
    merged
    .groupby(["ID", "alpha2", "year"], dropna=False)
    .agg(
        nationality=("nationality", exceptions),
        counts=("counts", "sum"),
    )
    .reset_index()
)

merged_agg = merged_agg[merged_agg["ID"].notna()]
merged_agg["ID"] = merged_agg["ID"].astype(int)

# Join population for the matching (country, year)
merged_agg = pd.merge(
    merged_agg,
    pop_long[["country-code", "year", "population"]],
    left_on=["ID", "year"],
    right_on=["country-code", "year"],
    how="left"
)

# Scale: books per million inhabitants
merged_agg["counts_raw"] = merged_agg["counts"]
merged_agg["counts"] = (
    merged_agg["counts"] / merged_agg["population"] * 1_000_000
).round(4)

# Warn about missing population data
missing_pop = merged_agg[merged_agg["population"].isna()]
if not missing_pop.empty:
    print("Missing population data for:")
    print(missing_pop[["nationality", "year"]].drop_duplicates().to_string())

merged_agg = merged_agg.drop(columns=["country-code", "population"])
merged_agg.to_csv("datasets/nat_date.csv", index=False)

print("Unmatched nationalities:")
print(grouped[grouped["matched_name"].isna()]["nationality"].unique())
