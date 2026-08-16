from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# CALCULATOR PAGES
# =========================================================

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")


@app.route("/scientific")
def scientific():
    return render_template("scientific.html")


@app.route("/mathematics")
def mathematics():
    return render_template("mathematics.html")


@app.route("/advanced-math")
def advanced_math():
    return render_template("advanced_math.html")


@app.route("/finance")
def finance():
    return render_template("finance.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/geometry")
def geometry():
    return render_template("geometry.html")


@app.route("/physics")
def physics():
    return render_template("physics.html")


@app.route("/converter")
def converter():
    return render_template("converter.html")


@app.route("/programmer")
def programmer():
    return render_template("programmer.html")


@app.route("/engineering")
def engineering():
    return render_template("engineering.html")


@app.route("/biology")
def biology():
    return render_template("biology.html")


@app.route("/chemistry")
def chemistry():
    return render_template("chemistry.html")


# =========================================================
# SCIENTIFIC CALCULATOR API
# =========================================================

@app.route("/api/scientific", methods=["POST"])
def scientific_api():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        expression = data.get(
            "expression",
            ""
        ).strip()

        angle_mode = data.get(
            "angle_mode",
            "DEG"
        ).upper()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Expression is empty"
            }), 400

        # -------------------------------------------------
        # Calculator symbol replacements
        # -------------------------------------------------

        expression = expression.replace("π", "pi")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")
        expression = expression.replace("√", "sqrt")

        # -------------------------------------------------
        # Mathematical functions
        # -------------------------------------------------

        functions = {

            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,

            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,

            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,

            "sqrt": sp.sqrt,

            "log": sp.log10,
            "ln": sp.log,

            "exp": sp.exp,
            "abs": sp.Abs,

            "factorial": sp.factorial,

            "floor": sp.floor,
            "ceil": sp.ceiling
        }

        # -------------------------------------------------
        # DEGREE MODE
        # -------------------------------------------------

        if angle_mode == "DEG":

            functions["sin"] = lambda value: sp.sin(
                value * sp.pi / 180
            )

            functions["cos"] = lambda value: sp.cos(
                value * sp.pi / 180
            )

            functions["tan"] = lambda value: sp.tan(
                value * sp.pi / 180
            )

            functions["asin"] = lambda value: (
                sp.asin(value) * 180 / sp.pi
            )

            functions["acos"] = lambda value: (
                sp.acos(value) * 180 / sp.pi
            )

            functions["atan"] = lambda value: (
                sp.atan(value) * 180 / sp.pi
            )

        # -------------------------------------------------
        # RADIAN MODE
        # -------------------------------------------------

        elif angle_mode == "RAD":

            functions["sin"] = sp.sin
            functions["cos"] = sp.cos
            functions["tan"] = sp.tan

            functions["asin"] = sp.asin
            functions["acos"] = sp.acos
            functions["atan"] = sp.atan

        # -------------------------------------------------
        # GRADIAN MODE
        # -------------------------------------------------

        elif angle_mode == "GRAD":

            functions["sin"] = lambda value: sp.sin(
                value * sp.pi / 200
            )

            functions["cos"] = lambda value: sp.cos(
                value * sp.pi / 200
            )

            functions["tan"] = lambda value: sp.tan(
                value * sp.pi / 200
            )

            functions["asin"] = lambda value: (
                sp.asin(value) * 200 / sp.pi
            )

            functions["acos"] = lambda value: (
                sp.acos(value) * 200 / sp.pi
            )

            functions["atan"] = lambda value: (
                sp.atan(value) * 200 / sp.pi
            )

        else:

            return jsonify({
                "success": False,
                "error": "Invalid angle mode"
            }), 400

        # -------------------------------------------------
        # Constants and functions
        # -------------------------------------------------

        local_variables = {
            **functions,
            "pi": sp.pi,
            "e": sp.E,
            "E": sp.E
        }

        # -------------------------------------------------
        # Calculate expression
        # -------------------------------------------------

        result = sp.sympify(
            expression,
            locals=local_variables
        )

        # -------------------------------------------------
        # Simplify
        # -------------------------------------------------

        result = sp.simplify(result)

        # -------------------------------------------------
        # Numeric result
        # -------------------------------------------------

        numeric_result = sp.N(
            result,
            15
        )

        # -------------------------------------------------
        # Return JSON
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "expression": expression,

            "result": str(
                numeric_result
            ),

            "exact": str(
                result
            )

        })

    except ZeroDivisionError:

        return jsonify({

            "success": False,

            "error": "Cannot divide by zero"

        }), 400

    except Exception as error:

        print(
            "Calculator Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": "Invalid mathematical expression"

        }), 400


# =========================================================
# API TEST
# =========================================================

@app.route("/api/test")
def test_api():

    return jsonify({

        "success": True,

        "message": "CalcWorld API is working!"

    })


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
