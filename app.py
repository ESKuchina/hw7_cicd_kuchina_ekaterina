from flask import Flask, jsonify, request
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
MODEL_VERSION = os.getenv("MODEL_VERSION", APP_VERSION)
PORT = int(os.getenv("PORT", "8000"))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "model_version": MODEL_VERSION
    })


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}
    x = payload.get("x", [])

    if not isinstance(x, list):
        return jsonify({
            "status": "error",
            "message": "Поле x должно быть списком чисел"
        }), 400

    try:
        values = [float(v) for v in x]
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Все элементы x должны быть числами"
        }), 400

    prediction = sum(values)

    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "model_version": MODEL_VERSION,
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
