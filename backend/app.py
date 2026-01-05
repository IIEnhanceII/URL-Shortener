from flask import Flask, request, jsonify, redirect
from db import get_connection
import random
import string

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def short_code_exists(short_code):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT 1 FROM dmforlink WHERE pipiurl = %s"
    cursor.execute(query, (short_code,))
    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists

def is_valid_url(url):
    if not url:
        return False
    return url.startswith("http://") or url.startswith("https://")

app = Flask(__name__)

@app.route("/")
def home():
    return "URL Shortener Backend Running"

@app.route("/health")
def health():
    return {"status": "ok"}

# 🔹 POST endpoint — creation flow
@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "long_url" not in data:
        return jsonify({"error": "long_url is required"}), 400

    long_url = data.get("long_url")

    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while short_code_exists(short_code):
        short_code = generate_short_code()

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO dmforlink (original, pipiurl)
    VALUES (%s, %s)
    """
    cursor.execute(insert_query, (long_url, short_code))
    conn.commit()

    cursor.close()
    conn.close()

    short_url = f"http://localhost:5000/{short_code}"

    return jsonify({"short_url": short_url}), 200

# 🔹 GET endpoint — usage flow (MUST BE LAST)
@app.route("/<short_code>")
def redirect_short_url(short_code):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT original FROM dmforlink WHERE pipiurl = %s"
    cursor.execute(query, (short_code,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
