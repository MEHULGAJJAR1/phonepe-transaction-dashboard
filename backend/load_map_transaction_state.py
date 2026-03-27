import os
import json
from db_connection import get_connection

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
path = os.path.join(base_path, "data", "map", "transaction", "hover", "country", "india", "state")

print("Reading from:", path)

connection = get_connection()
cursor = connection.cursor()

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = file.replace(".json", "")
                file_path = os.path.join(year_path, file)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    for item in data["data"]["hoverDataList"]:
                        district = item["name"]
                        count = item["metric"][0]["count"]
                        amount = item["metric"][0]["amount"]

                        cursor.execute("""
                            INSERT INTO map_transaction
                            (state, year, quarter, district, transaction_count, transaction_amount)
                            VALUES (%s,%s,%s,%s,%s,%s)
                        """, (state, year, quarter, district, count, amount))

connection.commit()
cursor.close()
connection.close()

print("Map State Transaction Data Inserted")