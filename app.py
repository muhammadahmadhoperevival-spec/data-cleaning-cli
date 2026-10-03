import numpy as np
import pandas as pd
import streamlit as st

from src.cleaner import impute

st.set_page_config(page_title="Data Cleaning Tool", page_icon="🧹", layout="wide")
st.title("🧹 Data Cleaning Tool")
st.write("Upload a CSV file, see which values are missing, and download a cleaned copy.")

with st.sidebar:
    st.header("Settings")
    strategy = st.radio("Numeric columns are filled with", ["median", "mean"])
    threshold = st.slider("Drop columns with more than this fraction missing",
                          0.1, 1.0, 0.5, 0.05)

file = st.file_uploader("Upload a CSV file", type="csv")

if file is None:
    st.info("Upload a CSV to get started. Try the Titanic dataset from the repo's data/raw folder.")
    st.stop()

df = pd.read_csv(file)
clean = impute(df, strategy, threshold)
dropped = sorted(set(df.columns) - set(clean.columns))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", len(df))
c2.metric("Columns", df.shape[1])
c3.metric("Missing before", int(df.isna().sum().sum()))
c4.metric("Missing after", int(clean.isna().sum().sum()))

if dropped:
    st.warning(f"Dropped columns (too many missing values): {', '.join(dropped)}")

left, right = st.columns(2)
with left:
    st.subheader("Missing values per column (before)")
    st.bar_chart(df.isna().sum())
with right:
    st.subheader("Missing values per column (after)")
    st.bar_chart(clean.isna().sum())

numeric_cols = [c for c in clean.select_dtypes("number").columns if c in df.columns]
if numeric_cols:
    st.subheader("Distribution of a numeric column")
    col = st.selectbox("Column", numeric_cols)
    edges = np.histogram_bin_edges(df[col].dropna(), bins=15)
    labels = [f"{edges[i]:.1f}-{edges[i + 1]:.1f}" for i in range(len(edges) - 1)]
    hist = pd.DataFrame({
        "before": np.histogram(df[col].dropna(), bins=edges)[0],
        "after": np.histogram(clean[col], bins=edges)[0],
    }, index=labels)
    st.bar_chart(hist)

st.subheader("Cleaned data (first 50 rows)")
st.dataframe(clean.head(50))
st.download_button("Download cleaned CSV", clean.to_csv(index=False),
                   "clean.csv", "text/csv")