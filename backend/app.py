from flask import Flask, request, jsonify, redirect, render_template
from db import insert_url, get_original, short_code_exists
import random
import string
import os
from flask_cors import CORS


BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    if not url:
        return False
    return url.startswith("http://") or url.startswith("https://")

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "URL Shortener Backend Running"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True)

    if not data or "long_url" not in data:
        return jsonify({"error": "long_url is required"}), 400

    long_url = data.get("long_url")

    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Collision-safe short code generation
    short_code = generate_short_code()
    while short_code_exists(short_code):
        short_code = generate_short_code()

    try:
        insert_url(long_url, short_code)
    except Exception:
        return jsonify({"error": "Server error"}), 500

    short_url = f"{BASE_URL}/{short_code}"
    return jsonify({"short_url": short_url}), 200


@app.route("/<short_code>")
def redirect_short_url(short_code):
    original = get_original(short_code)

    if original:
        return redirect(original, code=302)

    # Browser-friendly error page
    return render_template("not_found.html"), 404


if __name__ == "__main__":
    app.run()
