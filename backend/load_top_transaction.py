import os
import json
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

path = "../data/top/transaction/country/india/state"

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = file.replace(".json", "")
                file_path = os.path.join(year_path, file)

                with open(file_path) as f:
                    data = json.load(f)

                try:
                    for item in data["data"]["districts"]:
                        district = item["entityName"]
                        count = item["metric"]["count"]
                        amount = item["metric"]["amount"]

                        cursor.execute("""
                        INSERT INTO top_transaction
                        (state, district, year, quarter,
                         transaction_amount, transaction_count)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """, (state, district, year, quarter, amount, count))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Top Transaction Data Loaded")