from flask import Flask, render_template, request, jsonify
from db_connection import get_connection

app = Flask(__name__)

# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET"])
def home():

    year = request.args.get("year")
    state = request.args.get("state")
    ttype = request.args.get("type")

    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    connection = get_connection()
    cursor = connection.cursor()

    # Cards
    cursor.execute("SELECT SUM(transaction_amount) FROM aggregated_transaction")
    total_transaction = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(user_count) FROM aggregated_user")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(insurance_amount) FROM aggregated_insurance")
    total_insurance = cursor.fetchone()[0]

    # Dropdown Data
    cursor.execute("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year")
    years = cursor.fetchall()

    cursor.execute("SELECT DISTINCT state FROM map_transaction ORDER BY state")
    states = cursor.fetchall()

    cursor.execute("SELECT DISTINCT transaction_type FROM aggregated_transaction ORDER BY transaction_type")
    types = cursor.fetchall()

    # Filter Query
    query = """
    SELECT state, year, quarter, transaction_type,
    SUM(transaction_amount), SUM(transaction_count)
    FROM aggregated_transaction
    WHERE 1=1
    """

    params = []

    if year and year != "":
        query += " AND year=%s"
        params.append(year)

    if state and state != "":
        query += " AND state=%s"
        params.append(state)

    if ttype and ttype != "":
        query += " AND transaction_type=%s"
        params.append(ttype)

    query += """
    GROUP BY state, year, quarter, transaction_type
    LIMIT %s OFFSET %s
    """

    params.extend([per_page, offset])

    cursor.execute(query, params)
    table_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        total_transaction=total_transaction,
        total_users=total_users,
        total_insurance=total_insurance,
        table_data=table_data,
        years=years,
        states=states,
        types=types,
        year=year,
        state=state,
        ttype=ttype,
        page=page
    )


# ---------------- CHARTS PAGE ----------------
@app.route("/charts")
def charts():
    return render_template("charts.html")


# ---------------- YEARLY CHART API ----------------
@app.route("/api/yearly")
def yearly_chart():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT year, SUM(transaction_amount)
    FROM aggregated_transaction
    GROUP BY year
    ORDER BY year
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({
        "years": [i[0] for i in data],
        "amounts": [float(i[1]) for i in data]
    })


# ---------------- TYPE CHART API ----------------
@app.route("/api/types")
def type_chart():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT transaction_type, SUM(transaction_amount)
    FROM aggregated_transaction
    GROUP BY transaction_type
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({
        "types": [i[0] for i in data],
        "amounts": [float(i[1]) for i in data]
    })


# ---------------- MAP PAGE ----------------
@app.route("/map")
def map_insights():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT state, SUM(transaction_amount)
    FROM map_transaction
    GROUP BY state
    ORDER BY SUM(transaction_amount) DESC
    """)

    data = cursor.fetchall()

    states = [i[0] for i in data]
    amounts = [float(i[1]) for i in data]

    cursor.close()
    connection.close()

    return render_template("map.html", states=states, amounts=amounts)


# ---------------- TOP PERFORMERS ----------------
@app.route("/top")
def top_performers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT state, SUM(transaction_amount)
    FROM map_transaction
    GROUP BY state
    ORDER BY SUM(transaction_amount) DESC
    LIMIT 10
    """)
    top_states = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("top.html", top_states=top_states)


# ---------------- TOP STATES API ----------------
@app.route("/api/topstates")
def top_states_chart():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT state, SUM(transaction_amount)
    FROM map_transaction
    GROUP BY state
    ORDER BY SUM(transaction_amount) DESC
    LIMIT 10
    """)

    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify({
        "states": [i[0] for i in data],
        "amounts": [float(i[1]) for i in data]
    })


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run()



# from flask import Flask, render_template, request
# from db_connection import get_connection

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def home():

#     year = request.args.get("year")
#     state = request.args.get("state")
#     ttype = request.args.get("type")

#     page = request.args.get("page", 1, type=int)
#     per_page = 20
#     offset = (page - 1) * per_page

#     connection = get_connection()
#     cursor = connection.cursor()

#     # Cards
#     cursor.execute("SELECT SUM(transaction_amount) FROM aggregated_transaction")
#     total_transaction = cursor.fetchone()[0]

#     cursor.execute("SELECT SUM(registered_users) FROM aggregated_user")
#     total_users = cursor.fetchone()[0]

#     cursor.execute("SELECT SUM(insurance_amount) FROM aggregated_insurance")
#     total_insurance = cursor.fetchone()[0]

#     # Dropdown Data
#     cursor.execute("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year")
#     years = cursor.fetchall()

#     cursor.execute("SELECT DISTINCT state FROM map_transaction ORDER BY state")
#     states = cursor.fetchall()

#     cursor.execute("SELECT DISTINCT transaction_type FROM aggregated_transaction ORDER BY transaction_type")
#     types = cursor.fetchall()

#     # Filter Query
#     query = """
#     SELECT state, year, quarter, transaction_type,
#     SUM(transaction_amount), SUM(transaction_count)
#     FROM aggregated_transaction
#     WHERE 1=1
#     """

#     params = []

#     if year and year != "":
#         query += " AND year=%s"
#         params.append(year)

#     if state and state != "":
#         query += " AND state=%s"
#         params.append(state)

#     if ttype and ttype != "":
#         query += " AND transaction_type=%s"
#         params.append(ttype)

#     query += """
#     GROUP BY state, year, quarter, transaction_type
#     LIMIT %s OFFSET %s
#     """

#     params.extend([per_page, offset])

#     cursor.execute(query, params)
#     table_data = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return render_template(
#         "index.html",
#         total_transaction=total_transaction,
#         total_users=total_users,
#         total_insurance=total_insurance,
#         table_data=table_data,
#         years=years,
#         states=states,
#         types=types,
#         year=year,
#         state=state,
#         ttype=ttype,
#         page=page
#     )


# # Charts Page
# @app.route("/charts")
# def charts():
#     return render_template("charts.html")


# # API for Realtime Charts
# @app.route("/api/yearly")
# def yearly_chart():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#     SELECT year, SUM(transaction_amount)
#     FROM aggregated_transaction
#     GROUP BY year
#     ORDER BY year
#     """)

#     data = cursor.fetchall()
#     cursor.close()
#     connection.close()

#     return {
#         "years": [i[0] for i in data],
#         "amounts": [float(i[1]) for i in data]
#     }


# @app.route("/api/types")
# def type_chart():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#     SELECT transaction_type, SUM(transaction_amount)
#     FROM aggregated_transaction
#     GROUP BY transaction_type
#     """)

#     data = cursor.fetchall()
#     cursor.close()
#     connection.close()

#     return {
#         "types": [i[0] for i in data],
#         "amounts": [float(i[1]) for i in data]
#     }
# @app.route("/map")
# def map_insights():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#     SELECT state, SUM(transaction_amount)
#     FROM map_transaction
#     GROUP BY state
#     ORDER BY SUM(transaction_amount) DESC
#     """)

#     data = cursor.fetchall()

#     states = [i[0] for i in data]
#     amounts = [float(i[1]) for i in data]

#     cursor.close()
#     connection.close()

#     return render_template("map.html", states=states, amounts=amounts)


# @app.route("/top")
# def top_performers():
#     connection = get_connection()
#     cursor = connection.cursor()

#     # Top States
#     cursor.execute("""
#     SELECT state, SUM(transaction_amount)
#     FROM map_transaction
#     GROUP BY state
#     ORDER BY SUM(transaction_amount) DESC
#     LIMIT 10
#     """)
#     top_states = cursor.fetchall()

#     # Top Districts
#     cursor.execute("""
#     SELECT district, SUM(transaction_amount)
#     FROM top_transaction
#     GROUP BY district
#     ORDER BY SUM(transaction_amount) DESC
#     LIMIT 10
#     """)
#     top_districts = cursor.fetchall()

#     # Top Pincodes
#     cursor.execute("""
#     SELECT pincode, SUM(transaction_amount)
#     FROM top_transaction
#     GROUP BY pincode
#     ORDER BY SUM(transaction_amount) DESC
#     LIMIT 10
#     """)
#     top_pincodes = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return render_template(
#         "top.html",
#         top_states=top_states,
#         top_districts=top_districts,
#         top_pincodes=top_pincodes
#     )

# @app.route("/api/topstates")
# def top_states_chart():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#     SELECT state, SUM(transaction_amount)
#     FROM map_transaction
#     GROUP BY state
#     ORDER BY SUM(transaction_amount) DESC
#     LIMIT 10
#     """)

#     data = cursor.fetchall()
#     cursor.close()
#     connection.close()

#     return {
#         "states": [i[0] for i in data],
#         "amounts": [float(i[1]) for i in data]
#     }


# if __name__ == "__main__":
#     app.run(debug=True)
