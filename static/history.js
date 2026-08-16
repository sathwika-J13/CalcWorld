// =========================================================
// CALCWORLD SCIENTIFIC CALCULATOR
// =========================================================


// ---------------------------------------------------------
// VARIABLES
// ---------------------------------------------------------

const display = document.getElementById("display");

const result = document.getElementById("result");

const resultBox = document.getElementById("resultBox");

const historyList = document.getElementById("historyList");

let angleMode = "DEG";

let lastAnswer = 0;


// ---------------------------------------------------------
// INSERT VALUE
// ---------------------------------------------------------

function insertValue(value) {

    display.value += value;

    display.focus();
}


// ---------------------------------------------------------
// CLEAR DISPLAY
// ---------------------------------------------------------

function clearDisplay() {

    display.value = "";

    result.textContent = "0";

    resultBox.style.display = "none";

    display.focus();
}


// ---------------------------------------------------------
// DELETE LAST CHARACTER
// ---------------------------------------------------------

function deleteLast() {

    display.value = display.value.slice(0, -1);

    display.focus();
}


// ---------------------------------------------------------
// ANGLE MODE
// ---------------------------------------------------------

function setAngleMode(mode) {

    angleMode = mode;

    document.getElementById("degBtn")
        .classList.remove("active");

    document.getElementById("radBtn")
        .classList.remove("active");

    document.getElementById("gradBtn")
        .classList.remove("active");


    if (mode === "DEG") {

        document.getElementById("degBtn")
            .classList.add("active");

    }

    else if (mode === "RAD") {

        document.getElementById("radBtn")
            .classList.add("active");

    }

    else if (mode === "GRAD") {

        document.getElementById("gradBtn")
            .classList.add("active");

    }
}


// ---------------------------------------------------------
// CALCULATE
// ---------------------------------------------------------

async function calculate() {

    const expression = display.value.trim();


    if (!expression) {

        return;
    }


    result.textContent = "Calculating...";

    resultBox.style.display = "block";


    try {

        const response = await fetch(
            "/api/scientific",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    expression: expression,
                    angle_mode: angleMode
                })
            }
        );


        // -------------------------------------------------
        // Check HTTP response
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );
        }


        const data = await response.json();


        // -------------------------------------------------
        // Check API response
        // -------------------------------------------------

        if (!data.success) {

            throw new Error(
                data.error || "Calculation failed"
            );
        }


        // -------------------------------------------------
        // Display answer
        // -------------------------------------------------

        const answer = data.result;

        lastAnswer = Number(answer);

        result.textContent = answer;

        resultBox.style.display = "block";


        // -------------------------------------------------
        // Add history
        // -------------------------------------------------

        addToHistory(
            expression + " [" + angleMode + "]",
            answer
        );

    }


    catch (error) {

        console.error(
            "Scientific Calculator Error:",
            error
        );

        result.textContent =
            "Invalid calculation";

        resultBox.style.display =
            "block";
    }
}


// ---------------------------------------------------------
// HISTORY
// ---------------------------------------------------------

function addToHistory(
    expression,
    answer
) {

    const item =
        document.createElement("li");


    item.textContent =
        expression + " = " + answer;


    historyList.prepend(item);


    // Keep only latest 20 calculations

    while (
        historyList.children.length > 20
    ) {

        historyList.removeChild(
            historyList.lastChild
        );
    }
}


// ---------------------------------------------------------
// KEYBOARD SUPPORT
// ---------------------------------------------------------

display.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            calculate();
        }


        if (event.key === "Escape") {

            clearDisplay();
        }


        if (event.key === "Backspace") {

            return;
        }

    }
);


// ---------------------------------------------------------
// INITIALIZE
// ---------------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function() {

        setAngleMode("DEG");

        display.focus();

    }
);
