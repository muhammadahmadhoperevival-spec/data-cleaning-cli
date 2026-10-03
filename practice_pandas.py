import pandas as pd

df = pd.read_csv("data/raw/titanic.csv")

print(df.head())
print(df.shape)
df.info()
print(df.describe())
print(df.isna().sum())

print(df[df["Age"] > 60])
print(df.groupby("Sex")["Survived"].mean())
print(df.groupby("Pclass")["Survived"].mean())
print(df["Age"].mean(), df["Age"].median())

import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a.mean(), np.median(a))
print(np.where(a > 2, "high", "low"))