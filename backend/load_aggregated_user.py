import os
import json
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

path = "../data/aggregated/user/country/india/state"

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
                    users = data["data"]["aggregated"]["registeredUsers"]
                    appopens = data["data"]["aggregated"]["appOpens"]

                    cursor.execute("""
                    INSERT INTO aggregated_user
                    (state, year, quarter, registered_users, app_opens)
                    VALUES (%s,%s,%s,%s,%s)
                    """, (state, year, quarter, users, appopens))
                except:
                    pass

connection.commit()
cursor.close()
connection.close()

print("Aggregated User Data Loaded")