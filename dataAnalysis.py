import pandas as pd

df = pd.read_csv("merged1.csv")

print("Number of files:",df.shape[0])
df.drop_duplicates()
print("Number of unique files:",df["name"].nunique())
print("Number of repositories:",df["repo"].nunique())
