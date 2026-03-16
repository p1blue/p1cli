import polars as pl

df = pl.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [28, 35, 42, 29, 31],
        "department": ["Sales", "Engineering", "Sales", "Marketing", "Engineering"],
        "salary": [50000, 80000, 55000, 45000, 75000],
    }
)

filtered = df.filter(pl.col("age") > 30)

result = filtered.group_by("department").agg(
    pl.col("salary").mean().alias("mean_salary")
)

print(result)
