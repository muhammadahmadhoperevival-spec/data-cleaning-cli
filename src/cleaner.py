"""Data cleaning CLI: load a dataset, impute missing values, save a clean CSV."""
import argparse
from pathlib import Path

import pandas as pd


def load(path):
    """Load a CSV, Excel or JSON file into a DataFrame."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".json":
        return pd.read_json(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def impute(df, num_strategy="median", drop_threshold=0.5):
    """Return a cleaned copy of df.

    - removes duplicate rows
    - drops columns with more than `drop_threshold` fraction missing
    - fills numeric columns with the median (or mean)
    - fills text columns with the most common value (mode)
    """
    df = df.drop_duplicates().copy()

    ratio = df.isna().mean()
    df = df.drop(columns=ratio[ratio > drop_threshold].index)

    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            fill = df[col].median() if num_strategy == "median" else df[col].mean()
        else:
            mode = df[col].mode()
            fill = mode.iloc[0] if not mode.empty else "Unknown"
        df[col] = df[col].fillna(fill)
    return df


def main():
    parser = argparse.ArgumentParser(description="Impute missing values in a dataset.")
    parser.add_argument("input", help="Path to a CSV, Excel or JSON file")
    parser.add_argument("-o", "--output", help="Path for the cleaned CSV")
    parser.add_argument("--num-strategy", choices=["mean", "median"], default="median",
                        help="How to fill numeric columns (default: median)")
    parser.add_argument("--drop-threshold", type=float, default=0.5,
                        help="Drop columns with more than this fraction missing (default: 0.5)")
    args = parser.parse_args()

    df = load(args.input)
    missing = df.isna().sum()
    print(f"Rows, columns: {df.shape}")
    print(f"Missing values before:\n{missing[missing > 0]}\n")

    clean = impute(df, args.num_strategy, args.drop_threshold)
    dropped = sorted(set(df.columns) - set(clean.columns))
    print(f"Dropped columns: {dropped or 'none'}")
    print(f"Missing values after: {clean.isna().sum().sum()}")

    out = Path(args.output or f"data/processed/{Path(args.input).stem}_clean.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(out, index=False)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()