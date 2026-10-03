# Data Cleaning CLI

A small Python tool that loads a dataset (CSV, Excel or JSON), finds missing values, fills them in, and saves a clean CSV. It comes with a Streamlit web demo and a Jupyter notebook that explores the Titanic dataset before and after cleaning.

**Live demo:** https://YOUR-APP-NAME.streamlit.app  <!-- replace after deploying -->

## What the tool does

1. Loads a `.csv`, `.xlsx`, `.xls` or `.json` file.
2. Removes duplicate rows.
3. Drops columns with too many missing values (default: more than 50%).
4. Fills numeric columns with the **median** (or mean).
5. Fills text columns with the **mode** (most common value).
6. Saves the result to `data/processed/<name>_clean.csv`.

Why median and not mean? The median is not pulled around by extreme values, so it is the safer default.
Why drop a column like `Cabin` (77% missing)? Filling it would mean inventing most of its values.

## Project structure

```
data-cleaning-cli/
├── data/
│   ├── raw/              # input datasets (titanic.csv)
│   └── processed/        # cleaned output
├── notebooks/
│   └── eda.ipynb         # EDA with charts, before vs after cleaning
├── src/
│   ├── __init__.py
│   └── cleaner.py        # load(), impute() and the command line interface
├── app.py                # Streamlit demo
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/muhammadahmadhoperevival-spec/data-cleaning-cli.git
cd data-cleaning-cli

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

## Usage

### Command line

```bash
python src/cleaner.py data/raw/titanic.csv
```

Options:

| Option | Meaning | Default |
|---|---|---|
| `-o`, `--output` | Where to save the cleaned CSV | `data/processed/<name>_clean.csv` |
| `--num-strategy` | `median` or `mean` for numeric columns | `median` |
| `--drop-threshold` | Drop columns with more than this fraction missing | `0.5` |

Examples:

```bash
python src/cleaner.py data/raw/titanic.csv --num-strategy mean
python src/cleaner.py data/raw/titanic.csv --drop-threshold 0.9 -o cleaned.csv
python src/cleaner.py --help
```

Example output on the Titanic data:

```
Rows, columns: (891, 12)
Missing values before:
Age         177
Cabin       687
Embarked      2

Dropped columns: ['Cabin']
Missing values after: 0
Saved to data/processed/titanic_clean.csv
```

### Streamlit app

```bash
streamlit run app.py
```

Upload a CSV, choose mean or median, look at the missing-value charts before and after, and download the cleaned file.

### Notebook

```bash
jupyter notebook notebooks/eda.ipynb
```

Run all cells from the `notebooks` folder. The notebook shows missing values before and after cleaning, the Age distribution before and after imputation, survival rate by sex and class, and a correlation heatmap.

## Findings (Titanic)

- `Cabin` is 77% missing and was dropped; `Age` is 20% missing (filled with the median); `Embarked` has 2 missing values (filled with the mode).
- Women survived far more often than men (about 74% vs 19%).
- First class passengers survived more often than third class (about 63% vs 24%).
- These are correlations in the data, not proof of cause.

## Tech

Python, pandas, NumPy, matplotlib, seaborn, Streamlit, Jupyter.
