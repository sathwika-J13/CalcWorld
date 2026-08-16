from flask import Flask, render_template, request, jsonify
import math
import ast
import operator
from datetime import date

app = Flask(__name__)


# =========================================================
# SAFE BASIC CALCULATOR
# =========================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def safe_calculate(expression):
    expression = expression.replace("^", "**")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):

            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Invalid operator")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):

            value = evaluate(node.operand)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Invalid operator")

            return operation(value)

        raise ValueError("Invalid expression")

    return evaluate(tree)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SCIENTIFIC CALCULATOR PAGE
# =========================================================

@app.route("/scientific-calculator")
def scientific_page():
    return render_template("scientific.html")


# =========================================================
# PERCENTAGE CALCULATOR PAGE
# =========================================================

@app.route("/percentage-calculator")
def percentage_page():
    return render_template("percentage.html")


# =========================================================
# BASIC CALCULATOR API
# =========================================================

@app.route("/api/basic", methods=["POST"])
def basic():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        expression = str(
            data.get("expression", "")
        ).strip()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Expression is empty"
            }), 400

        result = safe_calculate(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return jsonify({
            "success": True,
            "result": result
        })

    except ZeroDivisionError:

        return jsonify({
            "success": False,
            "error": "Cannot divide by zero"
        }), 400

    except Exception as e:

        print("Basic calculator error:", e)

        return jsonify({
            "success": False,
            "error": "Invalid calculation"
        }), 400


# =========================================================
# SCIENTIFIC CALCULATOR API
# =========================================================

@app.route("/api/scientific", methods=["POST"])
def scientific():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        expression = str(
            data.get("expression", "")
        ).strip()

        angle_mode = str(
            data.get("angle_mode", "DEG")
        ).upper()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Expression is empty"
            }), 400

        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")
        expression = expression.replace("√", "sqrt")

        # -------------------------------------------------
        # TRIGONOMETRIC FUNCTIONS
        # -------------------------------------------------

        def sin(x):

            if angle_mode == "DEG":
                x = math.radians(x)

            return math.sin(x)


        def cos(x):

            if angle_mode == "DEG":
                x = math.radians(x)

            return math.cos(x)


        def tan(x):

            if angle_mode == "DEG":
                x = math.radians(x)

            return math.tan(x)


        def asin(x):

            result = math.asin(x)

            if angle_mode == "DEG":
                return math.degrees(result)

            return result


        def acos(x):

            result = math.acos(x)

            if angle_mode == "DEG":
                return math.degrees(result)

            return result


        def atan(x):

            result = math.atan(x)

            if angle_mode == "DEG":
                return math.degrees(result)

            return result


        # -------------------------------------------------
        # ALLOWED FUNCTIONS
        # -------------------------------------------------

        functions = {

            "sin": sin,
            "cos": cos,
            "tan": tan,

            "asin": asin,
            "acos": acos,
            "atan": atan,

            "sqrt": math.sqrt,

            "log": math.log10,
            "ln": math.log,

            "abs": abs,

            "exp": math.exp,

            "floor": math.floor,
            "ceil": math.ceil,

            "factorial": math.factorial,

            "pi": math.pi,
            "e": math.e
        }


        # -------------------------------------------------
        # CALCULATE
        # -------------------------------------------------

        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            functions
        )


        if isinstance(result, float):

            if result.is_integer():
                result = int(result)

            else:
                result = round(result, 12)


        return jsonify({

            "success": True,

            "result": result

        })


    except ZeroDivisionError:

        return jsonify({

            "success": False,

            "error":
                "Cannot divide by zero"

        }), 400


    except Exception as e:

        print(
            "Scientific calculator error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Invalid scientific calculation"

        }), 400


# =========================================================
# MATHEMATICS API
# =========================================================

@app.route("/api/mathematics", methods=["POST"])
def mathematics():

    try:

        data = request.get_json()

        operation = data.get(
            "operation"
        )

        value = float(
            data.get("value", 0)
        )


        if operation == "square":

            result = value ** 2


        elif operation == "cube":

            result = value ** 3


        elif operation == "sqrt":

            result = math.sqrt(value)


        elif operation == "factorial":

            if value < 0:
                raise ValueError(
                    "Factorial requires a positive number"
                )

            result = math.factorial(
                int(value)
            )


        elif operation == "absolute":

            result = abs(value)


        elif operation == "reciprocal":

            if value == 0:
                raise ValueError(
                    "Cannot divide by zero"
                )

            result = 1 / value


        else:

            raise ValueError(
                "Unknown operation"
            )


        return jsonify({

            "success": True,

            "result": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =========================================================
# PERCENTAGE API
# =========================================================

@app.route("/api/percentage", methods=["POST"])
def percentage():

    try:

        data = request.get_json()

        value = float(
            data.get("value", 0)
        )

        percent = float(
            data.get("percent", 0)
        )

        operation = data.get(
            "operation",
            "percent_of"
        )


        if operation == "percent_of":

            result = (
                value * percent / 100
            )


        elif operation == "increase":

            result = (
                value +
                value * percent / 100
            )


        elif operation == "decrease":

            result = (
                value -
                value * percent / 100
            )


        elif operation == "what_percent":

            if value == 0:

                raise ValueError(
                    "Cannot divide by zero"
                )

            result = (
                percent / value * 100
            )


        else:

            raise ValueError(
                "Invalid percentage operation"
            )


        return jsonify({

            "success": True,

            "result": round(
                result,
                12
            )

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =========================================================
# STATISTICS API
# =========================================================

@app.route("/api/statistics", methods=["POST"])
def statistics():

    try:

        data = request.get_json()

        numbers = data.get(
            "numbers",
            []
        )


        numbers = [

            float(x)

            for x in numbers

            if str(x).strip()

        ]


        if not numbers:

            raise ValueError(
                "Please enter numbers"
            )


        count = len(numbers)

        total = sum(numbers)

        mean = total / count


        sorted_numbers = sorted(
            numbers
        )


        if count % 2 == 0:

            median = (

                sorted_numbers[
                    count // 2 - 1
                ]

                +

                sorted_numbers[
                    count // 2
                ]

            ) / 2

        else:

            median = sorted_numbers[
                count // 2
            ]


        variance = sum(

            (x - mean) ** 2

            for x in numbers

        ) / count


        standard_deviation = math.sqrt(
            variance
        )


        return jsonify({

            "success": True,

            "count": count,

            "sum": total,

            "mean": mean,

            "median": median,

            "min": min(numbers),

            "max": max(numbers),

            "range":
                max(numbers) -
                min(numbers),

            "variance":
                variance,

            "standard_deviation":
                standard_deviation

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =========================================================
# NUMBER SYSTEM API
# =========================================================

@app.route("/api/number-system", methods=["POST"])
def number_system():

    try:

        data = request.get_json()

        value = str(
            data.get("value", "")
        ).strip()

        from_base = int(
            data.get(
                "from_base",
                10
            )
        )


        if from_base not in [
            2,
            8,
            10,
            16
        ]:

            raise ValueError(
                "Base must be 2, 8, 10 or 16"
            )


        number = int(
            value,
            from_base
        )


        return jsonify({

            "success": True,

            "binary":
                bin(number)[2:],

            "octal":
                oct(number)[2:],

            "decimal":
                str(number),

            "hexadecimal":
                hex(number)[2:].upper()

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                "Invalid number or base"

        }), 400


# =========================================================
# UNIT CONVERTER API
# =========================================================

@app.route("/api/unit", methods=["POST"])
def unit_converter():

    try:

        data = request.get_json()

        category = data.get(
            "category"
        )

        value = float(
            data.get("value", 0)
        )

        from_unit = data.get(
            "from_unit"
        )

        to_unit = data.get(
            "to_unit"
        )


        # -------------------------------------------------
        # LENGTH
        # -------------------------------------------------

        if category == "length":

            units = {

                "meter": 1,

                "kilometer": 1000,

                "centimeter": 0.01,

                "millimeter": 0.001,

                "mile": 1609.344,

                "yard": 0.9144,

                "foot": 0.3048,

                "inch": 0.0254

            }


            result = (

                value *

                units[from_unit]

                /

                units[to_unit]

            )


        # -------------------------------------------------
        # WEIGHT
        # -------------------------------------------------

        elif category == "weight":

            units = {

                "kilogram": 1,

                "gram": 0.001,

                "milligram": 0.000001,

                "pound": 0.45359237,

                "ounce": 0.0283495231

            }


            result = (

                value *

                units[from_unit]

                /

                units[to_unit]

            )


        # -------------------------------------------------
        # TEMPERATURE
        # -------------------------------------------------

        elif category == "temperature":

            if from_unit == to_unit:

                result = value


            elif (
                from_unit == "celsius"
                and
                to_unit == "fahrenheit"
            ):

                result = (
                    value * 9 / 5
                    + 32
                )


            elif (
                from_unit == "fahrenheit"
                and
                to_unit == "celsius"
            ):

                result = (
                    (value - 32)
                    * 5 / 9
                )


            elif (
                from_unit == "celsius"
                and
                to_unit == "kelvin"
            ):

                result = (
                    value + 273.15
                )


            elif (
                from_unit == "kelvin"
                and
                to_unit == "celsius"
            ):

                result = (
                    value - 273.15
                )


            elif (
                from_unit == "fahrenheit"
                and
                to_unit == "kelvin"
            ):

                result = (
                    (value - 32)
                    * 5 / 9
                    + 273.15
                )


            elif (
                from_unit == "kelvin"
                and
                to_unit == "fahrenheit"
            ):

                result = (
                    (value - 273.15)
                    * 9 / 5
                    + 32
                )


            else:

                raise ValueError(
                    "Invalid temperature units"
                )


        # -------------------------------------------------
        # TIME
        # -------------------------------------------------

        elif category == "time":

            units = {

                "second": 1,

                "minute": 60,

                "hour": 3600,

                "day": 86400

            }


            result = (

                value *

                units[from_unit]

                /

                units[to_unit]

            )


        else:

            raise ValueError(
                "Invalid category"
            )


        return jsonify({

            "success": True,

            "result":
                round(
                    result,
                    12
                )

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =========================================================
# AGE CALCULATOR API
# =========================================================

@app.route("/api/age", methods=["POST"])
def age_calculator():

    try:

        data = request.get_json()

        birth_year = int(
            data.get("birth_year")
        )

        birth_month = int(
            data.get("birth_month")
        )

        birth_day = int(
            data.get("birth_day")
        )


        birth_date = date(

            birth_year,

            birth_month,

            birth_day

        )


        today = date.today()


        years = (

            today.year -

            birth_date.year

        )


        if (

            today.month,

            today.day

        ) < (

            birth_date.month,

            birth_date.day

        ):

            years -= 1


        return jsonify({

            "success": True,

            "age": years,

            "message":
                f"You are {years} years old."

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                "Invalid birth date"

        }), 400


# =========================================================
# EMI CALCULATOR API
# =========================================================

@app.route("/api/emi", methods=["POST"])
def emi():

    try:

        data = request.get_json()

        principal = float(
            data.get("principal")
        )

        annual_rate = float(
            data.get("rate")
        )

        months = int(
            data.get("months")
        )


        if principal <= 0:

            raise ValueError(
                "Loan amount must be greater than zero"
            )


        if months <= 0:

            raise ValueError(
                "Loan period must be greater than zero"
            )


        monthly_rate = (
            annual_rate /
            12 /
            100
        )


        if monthly_rate == 0:

            monthly_payment = (
                principal /
                months
            )


        else:

            monthly_payment = (

                principal *

                monthly_rate *

                (1 + monthly_rate)
                ** months

                /

                (
                    (1 + monthly_rate)
                    ** months
                    - 1
                )

            )


        total_payment = (

            monthly_payment *
            months

        )


        total_interest = (

            total_payment -
            principal

        )


        return jsonify({

            "success": True,

            "monthly_payment":
                round(
                    monthly_payment,
                    2
                ),

            "total_payment":
                round(
                    total_payment,
                    2
                ),

            "total_interest":
                round(
                    total_interest,
                    2
                )

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =========================================================
# GOOGLE SEARCH CONSOLE VERIFICATION
# =========================================================

@app.route(
    "/google0c4dd368fd659561.html"
)
def google_verification():

    return app.send_static_file(
        "google0c4dd368fd659561.html"
    )


# =========================================================
# ROBOTS.TXT
# =========================================================

@app.route("/robots.txt")
def robots():

    return app.send_static_file(
        "robots.txt"
    )


# =========================================================
# SITEMAP
# =========================================================

@app.route("/sitemap.xml")
def sitemap():

    return app.send_static_file(
        "sitemap.xml"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "message":
            "CalcWorld is running"

    })


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "error": "Page not found"

    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success": False,

        "error":
            "Internal server error"

    }), 500


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )
