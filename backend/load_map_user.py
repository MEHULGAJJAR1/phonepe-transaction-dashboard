import os
import json
from db_connection import get_connection

path = "../data/map/user/hover/country/india"

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
                    for district, values in data["data"]["hoverData"].items():
                        registered_users = values["registeredUsers"]
                        app_opens = values["appOpens"]

                        cursor.execute("""
                            INSERT INTO map_user
                            (state, district, year, quarter, registered_users, app_opens)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, ("india", district, year, quarter, registered_users, app_opens))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Map User Data Inserted")