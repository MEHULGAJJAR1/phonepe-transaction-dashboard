import matplotlib.pyplot as plt
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

# Year Wise Transaction
cursor.execute("""
SELECT year, SUM(transaction_amount)
FROM aggregated_transaction
GROUP BY year
ORDER BY year
""")

data = cursor.fetchall()
years = [i[0] for i in data]
amounts = [i[1] for i in data]

plt.figure()
plt.bar(years, amounts)
plt.title("Year Wise Transaction")
plt.savefig("static/year_chart.png")

# Transaction Type
cursor.execute("""
SELECT transaction_type, SUM(transaction_amount)
FROM aggregated_transaction
GROUP BY transaction_type
""")

data = cursor.fetchall()
types = [i[0] for i in data]
amounts = [i[1] for i in data]

plt.figure()
plt.pie(amounts, labels=types, autopct='%1.1f%%')
plt.title("Transaction Type Distribution")
plt.savefig("static/type_chart.png")

# Top States
cursor.execute("""
SELECT state, SUM(transaction_amount)
FROM map_transaction
GROUP BY state
ORDER BY SUM(transaction_amount) DESC
LIMIT 10
""")

data = cursor.fetchall()
states = [i[0] for i in data]
amounts = [i[1] for i in data]

plt.figure()
plt.barh(states, amounts)
plt.title("Top States")
plt.savefig("static/top_states.png")

# Top Districts
cursor.execute("""
SELECT district, SUM(transaction_amount)
FROM top_transaction
GROUP BY district
ORDER BY SUM(transaction_amount) DESC
LIMIT 10
""")

data = cursor.fetchall()
districts = [i[0] for i in data]
amounts = [i[1] for i in data]

plt.figure()
plt.barh(districts, amounts)
plt.title("Top Districts")
plt.savefig("static/top_districts.png")

cursor.close()
connection.close()

print("Charts Generated")