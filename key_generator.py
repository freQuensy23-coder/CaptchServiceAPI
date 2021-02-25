#  Use this util to generate api_keys
from database import DataBase

db = DataBase()

print("Connected to DB")

access = int(input("Input necessary API level: "))

print(db.add_key(access=access))


