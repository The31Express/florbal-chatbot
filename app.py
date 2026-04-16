from flask import Flask, jsonify, request, render_template
import requests
import psycopg2
import os

API_KEY = "tsk-JgGoX7z7SYHhIaxAYc7gkg"
BASE_URL = "https://kurim.ithope.eu/v1"

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    return conn

@app.route("/ping")
def ping():
    return "pong"

@app.route("/status")
def status():
    return jsonify({
        "status": "ok",
        "author": "jan_janicek"
    })

@app.route("/save")
def save():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, msg TEXT);")
    cur.execute("INSERT INTO test (msg) VALUES ('ahoj z databaze');")

    conn.commit()
    cur.close()
    conn.close()

    return "ulozeno"

@app.route("/ai", methods=["POST"])
def ai():
    API_KEY = os.environ.get("OPENAI_API_KEY")
    BASE_URL = os.environ.get("OPENAI_BASE_URL")

    
    question = request.json.get("question", "")


    response = requests.post(
        BASE_URL + "/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gemma3:27b",
            "messages": [
                {
                    "role": "user",
                    "contemt": question
                }
            ]
        }
    )

    data = response.json()


    answer = data["choices"][0]["message"]["content"]

    return jsonify({"answer": answer})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
