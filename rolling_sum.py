import polars as pl

df = pl.DataFrame(
    {
        "date": pl.date_range(
            start=pl.date(2024, 1, 1),
            end=pl.date(2024, 1, 10),
            interval="1d",
            eager=True,
        ),
        "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    }
)

result = df.with_columns(
    pl.col("value").rolling_sum(window_size=3).alias("rolling_sum")
)
print(result)
