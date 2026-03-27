import os
import json
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

# ---------- Aggregated User ----------
path = "../data/aggregated/user/country/india"

for year in os.listdir(path):
    year_path = os.path.join(path, year)
    for file in os.listdir(year_path):
        if file.endswith(".json"):
            quarter = file.replace(".json", "")
            with open(os.path.join(year_path, file)) as f:
                data = json.load(f)
                try:
                    for i in data["data"]["usersByDevice"]:
                        brand = i["brand"]
                        count = i["count"]
                        percentage = i["percentage"]

                        cursor.execute("""
                            INSERT INTO aggregated_user
                            (state, year, quarter, brand, user_count, percentage)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, ("india", year, quarter, brand, count, percentage))
                except:
                    pass


# ---------- Aggregated Insurance ----------
path = "../data/aggregated/insurance/country/india"

for year in os.listdir(path):
    year_path = os.path.join(path, year)
    for file in os.listdir(year_path):
        if file.endswith(".json"):
            quarter = file.replace(".json", "")
            with open(os.path.join(year_path, file)) as f:
                data = json.load(f)
                try:
                    for i in data["data"]["transactionData"]:
                        name = i["name"]
                        count = i["paymentInstruments"][0]["count"]
                        amount = i["paymentInstruments"][0]["amount"]

                        cursor.execute("""
                            INSERT INTO aggregated_insurance
                            (state, year, quarter, insurance_type, insurance_count, insurance_amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, ("india", year, quarter, name, count, amount))
                except:
                    pass


connection.commit()
cursor.close()
connection.close()

print("All Aggregated Data Inserted")