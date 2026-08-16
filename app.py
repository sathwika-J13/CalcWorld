from flask import Flask, render_template, request, jsonify
import math
import ast
import operator

app = Flask(__name__)


# =========================================================
# SAFE BASIC CALCULATOR
# =========================================================

allowed_operators = {
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
    """
    Safely calculate basic mathematical expressions.
    Supports:
    + - * / % **
    parentheses
    """

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

            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Invalid operator")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)

            operation = allowed_operators.get(type(node.op))

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
# BASIC CALCULATOR API
# =========================================================

@app.route("/api/basic", methods=["POST"])
def basic_calculation():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        expression = data.get("expression")

        if expression is None:
            return jsonify({
                "error": "Expression is required"
            }), 400

        expression = str(expression).strip()

        if not expression:
            return jsonify({
                "error": "Expression is empty"
            }), 400

        result = safe_calculate(expression)

        if isinstance(result, float):

            if result.is_integer():
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

        print("BASIC ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": "Invalid calculation"
        }), 400


# =========================================================
# SCIENTIFIC CALCULATOR
# =========================================================

@app.route("/api/scientific", methods=["POST"])
def scientific_calculation():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        expression = data.get("expression", "").strip()
        angle_mode = data.get("angle_mode", "DEG")

        if not expression:
            return jsonify({
                "error": "Expression is empty"
            }), 400

        # Convert common mathematical symbols
        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")
        expression = expression.replace("√", "sqrt")

        # Angle conversion
        def sin(x):
            if angle_mode == "DEG":
                return math.sin(math.radians(x))
            return math.sin(x)

        def cos(x):
            if angle_mode == "DEG":
                return math.cos(math.radians(x))
            return math.cos(x)

        def tan(x):
            if angle_mode == "DEG":
                return math.tan(math.radians(x))
            return math.tan(x)

        functions = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,

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

        # Evaluate scientific expression
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

        print("SCIENTIFIC ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": "Invalid scientific calculation"
        }), 400


# =========================================================
# MATHEMATICS API
# =========================================================

@app.route("/api/mathematics", methods=["POST"])
def mathematics():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        operation = data.get("operation")
        value = data.get("value")

        if operation == "square":

            result = float(value) ** 2

        elif operation == "cube":

            result = float(value) ** 3

        elif operation == "sqrt":

            result = math.sqrt(float(value))

        elif operation == "factorial":

            result = math.factorial(int(value))

        elif operation == "percentage":

            result = float(value) / 100

        else:

            return jsonify({
                "success": False,
                "error": "Unknown operation"
            }), 400

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        print("MATHEMATICS ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": "Invalid mathematical operation"
        }), 400


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "message": "CalcWorld API is working"
    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
