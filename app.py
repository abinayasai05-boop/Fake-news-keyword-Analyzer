from flask import Flask, render_template, request, jsonify
from analyzer import analyze_text

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Please enter a news headline or article."
        }), 400

    result = analyze_text(text)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)