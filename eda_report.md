# Exploratory Data Analysis: International Bestsellers

This report presents the findings from the exploratory data analysis of the `international_bestsellers.csv` dataset.

## Dataset Overview
- **Total Rows:** 7910
- **Total Columns:** 10
- **Columns:** `date`, `country`, `rank`, `title`, `author`, `nationality`, `gender`, `entry_id`, `publisher`, `publication_country`
- **Date Range:** 2013-06-01 to 2024-03-01

## Missing Values
The dataset is largely complete, with only a few missing values:
- `rank`: 1 missing
- `title`: 6 missing
- `author`: 12 missing
- `nationality`: 12 missing
- `gender`: 12 missing
- `publication_country`: 23 missing

## Dealing with Co-Authorship 
In the raw dataset, books written by multiple co-authors have their individual genders and nationalities joined together by a semicolon (for example, `m; w` or `Sweden; Sweden`). This led to mixed demographic categories in the initial visualization. 

To provide a more accurate evaluation of author representation, the data for **Gender** and **Nationality** has been cleaned: entries with multiple authors have been _exploded_ (split) so each individual author is mapped to the final totals, giving us the true demographic distribution.

## Unique Entities
- **Unique Authors:** 1902
- **Unique Books:** 3754
- **Unique Publishers:** 750
- **Unique Countries (List Source):** 45

## Summary Statistics

### Top 10 Bestselling Authors
1. Elena Ferrante (120 entries)
2. Stephen King (87 entries)
3. Joël Dicker (87 entries)
4. John Grisham (84 entries)
5. Guillaume Musso (80 entries)
6. Paula Hawkins (77 entries)
7. Ken Follett (74 entries)
8. Jojo Moyes (74 entries)
9. Andrea Camilleri (70 entries)
10. Delia Owens (59 entries)

### Top 10 Bestselling Books
1. The Girl on the Train (62 entries)
2. My Brilliant Friend (61 entries)
3. Where The Crawdads Sing (60 entries)
4. All the Light We Cannot See (37 entries)
5. Origin (36 entries)
6. Fresh Water For Flowers (34 entries)
7. The Midnight Library (27 entries)
8. Homeland (26 entries)
9. The Goldfinch (25 entries)
10. After You (24 entries)

### Top 10 Nationalities (Exploded count)
1. United States (2139)
2. Italy (1074)
3. France (1061)
4. United Kingdom (875)
5. Spain (807)
6. Germany (604)
7. Sweden (209)
8. Switzerland (118)
9. Japan (110)
10. Australia (110)

## Visualizations

### Gender Distribution
![Gender Distribution](./assets/gender_distribution.png)

### Top 10 Nationalities
![Top 10 Nationalities](./assets/top_nationalities.png)

### Top 10 Countries with Most Bestseller Entries
![Top 10 Countries](./assets/top_countries.png)

### Top 10 Publishers
![Top 10 Publishers](./assets/top_publishers.png)
