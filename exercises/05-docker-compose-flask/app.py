import os

import mysql.connector
import redis
from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=3306,
        user=os.getenv("MYSQL_USER", "appuser"),
        password=os.getenv("MYSQL_PASSWORD", "apppassword"),
        database=os.getenv("MYSQL_DATABASE", "compose_demo"),
        connection_timeout=5
    )


@app.route("/")
def home():
    connection = None
    cursor = None

    try:
        # Increment the visit counter stored in Redis.
        redis_visits = redis_client.incr("page_visits")

        # Record this visit in MySQL.
        connection = get_mysql_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("INSERT INTO visits () VALUES ()")
        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM visits")
        mysql_visits = cursor.fetchone()[0]

        return jsonify({
            "message": "Flask + Redis + MySQL are working!",
            "redis_visit_count": redis_visits,
            "mysql_total_visits": mysql_visits
        })

    except Exception:
        app.logger.exception("Failed to process visit")
        return jsonify({
            "error": "Unable to connect to the backing services"
        }), 503

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
