# server.py
import os
import sqlite3

from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    user_id = request.args.get("id")  # SOURCE : entrée utilisateur
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # FAILLE 1 (injection SQL) : l'entrée est concaténée dans la requête
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)  # SINK
    return cursor.fetchall()


@app.route("/ping")
def ping_host():
    target = request.args.get("ip")  # SOURCE
    # FAILLE 2 (injection de commande) : l'entrée part dans un shell
    os.system("ping -c 1 " + target)  # SINK
    return "Ping triggered"


if __name__ == "__main__":
    app.run(port=5000)
