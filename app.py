from flask import Flask, render_template, request, jsonify
import sympy as sp
import math

app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# BASIC CALCULATOR PAGE
# =========================================================

@app.route("/basic")
def basic():
    return render_template("basic.html")


# =========================================================
# SCIENTIFIC CALCULATOR PAGE
# =========================================================

@app.route("/scientific")
def scientific_page():
    return render_template("scientific.html")


# =========================================================
# MATHEMATICS PAGE
# =========================================================

@app.route("/mathematics")
def mathematics_page():
    return render_template("mathematics.html")


# =========================================================
# UNIT CONVERTER PAGE
# =========================================================

@app.route("/converter")
def converter_page():
    return render_template("converter.html")


# =========================================================
# SCIENTIFIC CALCULATOR API
# =========================================================

@app.route("/api/scientific", methods=["POST"])
def scientific():

    try:

        data = request.get_json(silent=True) or {}

        expression = str(
            data.get("expression", "")
        ).strip()

        angle_mode = str(
            data.get("angle_mode", "DEG")
        ).upper()


        if not expression:

            return jsonify({
                "error": "Expression is empty"
            }), 400


        # ---------------------------------------------
        # Convert calculator symbols
        # ---------------------------------------------

        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")


        # ---------------------------------------------
        # Percentage
        # ---------------------------------------------

        expression = expression.replace("%", "/100")


        # ---------------------------------------------
        # Trigonometric functions
        # ---------------------------------------------

        if angle_mode == "DEG":

            def sin_deg(x):
                return sp.sin(sp.pi * x / 180)

            def cos_deg(x):
                return sp.cos(sp.pi * x / 180)

            def tan_deg(x):
                return sp.tan(sp.pi * x / 180)

            allowed_functions = {

                "sin": sin_deg,
                "cos": cos_deg,
                "tan": tan_deg,

                "asin": sp.asin,
                "acos": sp.acos,
                "atan": sp.atan,

            }

        else:

            allowed_functions = {

                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,

                "asin": sp.asin,
                "acos": sp.acos,
                "atan": sp.atan,

            }


        # ---------------------------------------------
        # Other functions
        # ---------------------------------------------

        allowed_functions.update({

            "sqrt": sp.sqrt,

            "log": sp.log10,

            "ln": sp.log,

            "abs": sp.Abs,

            "exp": sp.exp,

            "factorial": sp.factorial,

        })


        # ---------------------------------------------
        # Constants
        # ---------------------------------------------

        allowed_symbols = {

            "pi": sp.pi,

            "e": sp.E,

        }


        allowed_symbols.update(
            allowed_functions
        )


        # ---------------------------------------------
        # Calculate
        # ---------------------------------------------

        result = sp.sympify(
            expression,
            locals=allowed_symbols
        )


        result = sp.N(
            result,
            12
        )


        # ---------------------------------------------
        # Format result
        # ---------------------------------------------

        if result.is_real:

            value = float(result)


            if math.isfinite(value):

                if value.is_integer():

                    output = str(
                        int(value)
                    )

                else:

                    output = str(value)

            else:

                output = str(result)

        else:

            output = str(result)


        return jsonify({

            "result": output

        })


    except Exception as error:

        return jsonify({

            "error": str(error)

        }), 400


# =========================================================
# MATHEMATICS API
# =========================================================

@app.route("/api/mathematics", methods=["POST"])
def mathematics_api():

    try:

        data = request.get_json(silent=True) or {}

        expression = str(
            data.get("expression", "")
        ).strip()


        if not expression:

            return jsonify({
                "error": "Expression is empty"
            }), 400


        expression = expression.replace(
            "×", "*"
        )

        expression = expression.replace(
            "÷", "/"
        )

        expression = expression.replace(
            "−", "-"
        )

        expression = expression.replace(
            "^", "**"
        )


        result = sp.sympify(
            expression
        )


        result = sp.N(
            result,
            12
        )


        return jsonify({

            "result": str(result)

        })


    except Exception as error:

        return jsonify({

            "error": str(error)

        }), 400


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "application": "CalcWorld"

    })


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "error": "Page not found"

    }), 404


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
