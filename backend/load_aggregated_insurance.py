import os
import json
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

path = "../data/aggregated/insurance/country/india/state"

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
                    for item in data["data"]["transactionData"]:
                        count = item["paymentInstruments"][0]["count"]
                        amount = item["paymentInstruments"][0]["amount"]

                        cursor.execute("""
                        INSERT INTO aggregated_insurance
                        (state, year, quarter, insurance_amount, insurance_count)
                        VALUES (%s,%s,%s,%s,%s)
                        """, (state, year, quarter, amount, count))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Aggregated Insurance Data Loaded")