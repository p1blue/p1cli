import polars as pl

df = pl.DataFrame(
    {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "value": [2, 8, 3, 7, 1, 9, 4, 6, 5, 10],
        "category": ["A", "B", "A", "B", "C", "A", "B", "C", "A", "B"],
    }
)

result = (
    df.lazy()
    .filter(pl.col("value") > 5)
    .group_by("category")
    .agg(pl.col("value").sum().alias("total"))
    .collect()
)

print(result)
