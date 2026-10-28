import os
from typing import Any

import psycopg2
from flask import Flask, jsonify, request


app = Flask(__name__)

REGNO = os.getenv("REGNO", "202401100100091")
APP_VERSION = os.getenv("APP_VERSION", "0.1")
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("DB_NAME", "festdb"),
    "user": os.getenv("DB_USER", "festuser"),
    "password": os.getenv("DB_PASSWORD", ""),
}


def get_connection() -> Any:
    return psycopg2.connect(**DB_CONFIG, connect_timeout=3)


def ensure_schema(connection: Any) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                event TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
    connection.commit()


@app.get("/api/health")
def health() -> Any:
    database = False
    try:
        connection = get_connection()
        connection.close()
        database = True
    except psycopg2.Error:
        database = False
    return jsonify({"regno": REGNO, "database": database, "version": APP_VERSION})


@app.get("/api/registrations")
def registrations() -> Any:
    connection = get_connection()
    try:
        ensure_schema(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, event FROM registrations ORDER BY id"
            )
            rows = cursor.fetchall()
        return jsonify(
            [{"id": row[0], "name": row[1], "event": row[2]} for row in rows]
        )
    finally:
        connection.close()


@app.post("/api/registrations")
def create_registration() -> Any:
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    event = str(data.get("event", "")).strip()
    if not name or not event:
        return jsonify({"error": "name and event are required"}), 400

    connection = get_connection()
    try:
        ensure_schema(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO registrations (name, event) VALUES (%s, %s) "
                "RETURNING id, name, event",
                (name, event),
            )
            row = cursor.fetchone()
        connection.commit()
        return jsonify({"id": row[0], "name": row[1], "event": row[2]}), 201
    finally:
        connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)