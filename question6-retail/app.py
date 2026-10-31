from flask import Flask, jsonify
import mysql.connector
import redis
import os
import json
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "retailuser"),
    "password": os.getenv("DB_PASSWORD", "retailpass"),
    "database": os.getenv("DB_NAME", "retaildb"),
    "connection_timeout": 5
}

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
    socket_connect_timeout=3
)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialise_database():
    """Create the sales table and insert sample records."""
    for attempt in range(30):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    product VARCHAR(100),
                    quantity INT,
                    unit_price DECIMAL(10, 2)
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM sales")
            count = cursor.fetchone()[0]

            if count == 0:
                records = [
                    (1001, "Coffee", 2, 4.50),
                    (1002, "Headphones", 1, 79.99),
                    (1003, "Notebook", 3, 2.50),
                    (1001, "Water Bottle", 1, 12.00)
                ]

                cursor.executemany("""
                    INSERT INTO sales
                    (order_id, product, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                """, records)

            conn.commit()
            cursor.close()
            conn.close()

            print("Database initialised successfully.")
            return

        except mysql.connector.Error as error:
            print(f"Database not ready (attempt {attempt + 1}): {error}")
            time.sleep(2)

    raise RuntimeError("Could not connect to MySQL.")


@app.route("/")
def home():
    return jsonify({"message": "Retail Analytics Service is running"})


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()

        cache.ping()

        return jsonify({
            "status": "healthy",
            "mysql": "connected",
            "redis": "connected"
        })

    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "error": str(error)
        }), 503


@app.route("/sales/stats")
def sales_stats():
    try:
        cached_data = cache.get("retail:sales:stats")

        if cached_data:
            result = json.loads(cached_data)
            result["cache"] = "HIT"
            return jsonify(result)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT order_id) AS total_orders,
                SUM(quantity) AS items_sold,
                SUM(quantity * unit_price) AS total_revenue
            FROM sales
        """)

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        revenue = float(row["total_revenue"] or 0)
        orders = int(row["total_orders"] or 0)

        result = {
            "total_orders": orders,
            "items_sold": int(row["items_sold"] or 0),
            "total_revenue": round(revenue, 2),
            "average_order_value": round(revenue / orders, 2) if orders else 0
        }

        cache.setex(
            "retail:sales:stats",
            30,
            json.dumps(result)
        )

        result["cache"] = "MISS"
        return jsonify(result)

    except Exception as error:
        return jsonify({"error": str(error)}), 503


if __name__ == "__main__":
    initialise_database()
    app.run(host="0.0.0.0", port=5000)