import matplotlib.pyplot as plt
from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

# Year wise transaction
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
plt.savefig("static/charts/year_transaction.png")

# Payment types
cursor.execute("""
SELECT transaction_type, SUM(transaction_amount)
FROM aggregated_transaction
GROUP BY transaction_type
""")

data = cursor.fetchall()
types = [i[0] for i in data]
amounts = [i[1] for i in data]

plt.figure()
plt.bar(types, amounts)
plt.title("Transaction Types")
plt.xticks(rotation=45)
plt.savefig("static/charts/payment_type.png")

# Top states
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
plt.savefig("static/charts/top_states.png")

cursor.close()
connection.close()

print("Charts Generated Successfully")