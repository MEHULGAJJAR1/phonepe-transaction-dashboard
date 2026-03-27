import os
import json
from db_connection import get_connection

# Absolute path (important)
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
path = os.path.join(base_path, "data", "aggregated", "transaction", "state")

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

                    for t in data["data"]["transactionData"]:
                        ttype = t["name"]

                        for d in t["paymentInstruments"]:
                            count = d["count"]
                            amount = d["amount"]

                            cursor.execute("""
                                INSERT INTO aggregated_transaction
                                (state, year, quarter, transaction_type, transaction_count, transaction_amount)
                                VALUES (%s,%s,%s,%s,%s,%s)
                            """, (state, year, quarter, ttype, count, amount))

connection.commit()
cursor.close()
connection.close()

print("State Data Inserted Successfully")