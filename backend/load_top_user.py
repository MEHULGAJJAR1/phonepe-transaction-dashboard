import os
import json
from db_connection import get_connection

path = "../data/top/user/country/india"

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
                        district = i["name"]
                        users = i["registeredUsers"]

                        cursor.execute("""
                            INSERT INTO top_user
                            (state, district, year, quarter, registered_users)
                            VALUES (%s, %s, %s, %s, %s)
                        """, ("india", district, year, quarter, users))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Top User Data Inserted")