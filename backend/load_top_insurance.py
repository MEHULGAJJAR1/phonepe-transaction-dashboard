import os
import json
from db_connection import get_connection

path = "../data/top/insurance/country/india"

connection = get_connection()
cursor = connection.cursor()

for year in os.listdir(path):
    year_path = os.path.join(path, year)
    
    for file in os.listdir(year_path):
        if file.endswith(".json"):
            quarter = file.replace(".json", "")
            
            with open(os.path.join(year_path, file)) as f:
                data = json.load(f)

                try:
                    for i in data["data"]["districts"]:
                        district = i["entityName"]
                        count = i["metric"]["count"]
                        amount = i["metric"]["amount"]

                        cursor.execute("""
                            INSERT INTO top_insurance
                            (state, district, year, quarter, insurance_count, insurance_amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, ("india", district, year, quarter, count, amount))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Top Insurance Data Inserted")