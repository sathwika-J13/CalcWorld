from flask import Flask, render_template, request, jsonify
import sympy as sp
import math

app = Flask(__name__)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# SCIENTIFIC CALCULATOR
# -----------------------------
@app.route("/api/scientific", methods=["POST"])
def scientific():
    try:
        data = request.get_json()

        expression = data.get("expression", "").strip()
        angle_mode = data.get("angle_mode", "DEG")

        if not expression:
            return jsonify({"error": "Empty expression"}), 400

        # Convert calculator symbols to SymPy syntax
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")

        # Convert percentage
        expression = expression.replace("%", "/100")

        # Angle conversion
        if angle_mode == "DEG":
            sin_func = lambda x: sp.sin(sp.pi * x / 180)
            cos_func = lambda x: sp.cos(sp.pi * x / 180)
            tan_func = lambda x: sp.tan(sp.pi * x / 180)
        else:
            sin_func = sp.sin
            cos_func = sp.cos
            tan_func = sp.tan

        # Allowed functions
        allowed = {
            "sin": sin_func,
            "cos": cos_func,
            "tan": tan_func,
            "sqrt": sp.sqrt,
            "log": sp.log10,
            "ln": sp.log,
            "abs": sp.Abs,
            "exp": sp.exp,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "factorial": sp.factorial,
            "pi": sp.pi,
            "e": sp.E,
        }

        # Evaluate expression
        result = sp.sympify(expression, locals=allowed)

        # Numerical result
        result = sp.N(result, 12)

        # Remove unnecessary decimal .0
        if result.is_real:
            value = float(result)

            if value.is_integer():
                output = str(int(value))
            else:
                output = str(value)
        else:
            output = str(result)

        return jsonify({
            "result": output
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# -----------------------------
# SIMPLE MATHEMATICS API
# -----------------------------
@app.route("/api/mathematics", methods=["POST"])
def mathematics():
    try:
        data = request.get_json()
        expression = data.get("expression", "")

        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")

        result = sp.sympify(expression)

        return jsonify({
            "result": str(sp.N(result, 12))
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
