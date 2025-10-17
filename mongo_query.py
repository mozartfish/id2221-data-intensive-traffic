from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client["trafiklab"]
docs = list(db.departures.find().limit(5000))
df = pd.DataFrame(docs)

print("Columns:", df.columns.tolist())
print("\nSample document:")
print(docs[0])
print("\nDataFrame:")
print(df)