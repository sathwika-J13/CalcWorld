from flask import Flask, render_template, request, jsonify
import sympy as sp


app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SCIENTIFIC CALCULATOR
# =========================================================

@app.route("/scientific")
def scientific():
    return render_template("scientific.html")


# =========================================================
# MATHEMATICS CALCULATOR
# =========================================================

@app.route("/mathematics")
def mathematics():
    return render_template("mathematics.html")


# =========================================================
# SCIENTIFIC CALCULATOR API
# =========================================================

@app.route("/api/scientific", methods=["POST"])
def scientific_api():

    try:

        # Get JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400


        # Get expression
        expression = data.get(
            "expression",
            ""
        ).strip()


        # Get angle mode
        angle_mode = data.get(
            "angle_mode",
            "DEG"
        ).upper()


        # -------------------------------------------------
        # Check empty expression
        # -------------------------------------------------

        if not expression:

            return jsonify({
                "success": False,
                "error": "Expression is empty"
            }), 400


        # -------------------------------------------------
        # Replace calculator symbols
        # -------------------------------------------------

        expression = expression.replace(
            "π",
            "pi"
        )

        expression = expression.replace(
            "×",
            "*"
        )

        expression = expression.replace(
            "÷",
            "/"
        )

        expression = expression.replace(
            "^",
            "**"
        )

        expression = expression.replace(
            "√",
            "sqrt"
        )


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

            functions["sin"] = lambda value: (
                sp.sin(
                    value * sp.pi / 180
                )
            )

            functions["cos"] = lambda value: (
                sp.cos(
                    value * sp.pi / 180
                )
            )

            functions["tan"] = lambda value: (
                sp.tan(
                    value * sp.pi / 180
                )
            )

            functions["asin"] = lambda value: (
                sp.asin(value)
                * 180
                / sp.pi
            )

            functions["acos"] = lambda value: (
                sp.acos(value)
                * 180
                / sp.pi
            )

            functions["atan"] = lambda value: (
                sp.atan(value)
                * 180
                / sp.pi
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

            functions["sin"] = lambda value: (
                sp.sin(
                    value * sp.pi / 200
                )
            )

            functions["cos"] = lambda value: (
                sp.cos(
                    value * sp.pi / 200
                )
            )

            functions["tan"] = lambda value: (
                sp.tan(
                    value * sp.pi / 200
                )
            )

            functions["asin"] = lambda value: (
                sp.asin(value)
                * 200
                / sp.pi
            )

            functions["acos"] = lambda value: (
                sp.acos(value)
                * 200
                / sp.pi
            )

            functions["atan"] = lambda value: (
                sp.atan(value)
                * 200
                / sp.pi
            )


        # -------------------------------------------------
        # INVALID ANGLE MODE
        # -------------------------------------------------

        else:

            return jsonify({
                "success": False,
                "error": "Invalid angle mode"
            }), 400


        # -------------------------------------------------
        # Safe mathematical constants
        # -------------------------------------------------

        local_variables = {

            **functions,

            "pi": sp.pi,

            "e": sp.E,

            "E": sp.E

        }


        # -------------------------------------------------
        # Parse expression
        # -------------------------------------------------

        result = sp.sympify(
            expression,
            locals=local_variables
        )


        # -------------------------------------------------
        # Simplify result
        # -------------------------------------------------

        result = sp.simplify(
            result
        )


        # -------------------------------------------------
        # Numeric result
        # -------------------------------------------------

        numeric_result = sp.N(
            result,
            15
        )


        # -------------------------------------------------
        # Return result
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

            "error":
                "Cannot divide by zero"

        }), 400


    except Exception as error:

        print(
            "Calculator Error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Invalid mathematical expression"

        }), 400


# =========================================================
# TEST API
# =========================================================

@app.route("/api/test")
def test_api():

    return jsonify({

        "success": True,

        "message":
            "CalcWorld API is working!"

    })


# =========================================================
# START FLASK SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )