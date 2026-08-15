/* ==================================================
   CALCWORLD - CALCULATION HISTORY
================================================== */


/*
   Storage key
*/

const HISTORY_KEY =
    "calcworld_history";



/* ==================================================
   GET HISTORY
================================================== */

function getHistory() {

    try {

        const savedHistory =
            localStorage.getItem(
                HISTORY_KEY
            );


        if (!savedHistory) {

            return [];

        }


        const history =
            JSON.parse(
                savedHistory
            );


        if (!Array.isArray(history)) {

            return [];

        }


        return history;

    }

    catch (error) {

        console.error(
            "Unable to read history:",
            error
        );

        return [];

    }

}



/* ==================================================
   SAVE HISTORY
================================================== */

function saveHistory(history) {

    try {

        localStorage.setItem(
            HISTORY_KEY,
            JSON.stringify(history)
        );

    }

    catch (error) {

        console.error(
            "Unable to save history:",
            error
        );

    }

}



/* ==================================================
   ADD CALCULATION
================================================== */

function addToHistory(
    expression,
    result
) {

    /*
       Don't save empty calculations.
    */

    if (
        expression === undefined ||
        result === undefined
    ) {

        return;

    }


    const cleanExpression =
        String(expression).trim();


    const cleanResult =
        String(result).trim();


    if (
        cleanExpression === "" ||
        cleanResult === ""
    ) {

        return;

    }


    /*
       Get existing history.
    */

    const history =
        getHistory();


    /*
       Add newest calculation
       to the beginning.
    */

    history.unshift({

        expression:
            cleanExpression,

        result:
            cleanResult,

        time:
            new Date().toLocaleString()

    });


    /*
       Keep maximum 100 calculations.
    */

    if (history.length > 100) {

        history.splice(
            100
        );

    }


    /*
       Save.
    */

    saveHistory(history);


    /*
       Update screen.
    */

    displayHistory();

}



/* ==================================================
   DISPLAY HISTORY
================================================== */

function displayHistory() {

    const historyContainer =
        document.getElementById(
            "historyList"
        );


    /*
       If this page doesn't have
       history section, stop.
    */

    if (!historyContainer) {

        return;

    }


    const history =
        getHistory();


    /*
       Clear current list.
    */

    historyContainer.innerHTML =
        "";


    /*
       No history.
    */

    if (
        history.length === 0
    ) {

        historyContainer.innerHTML =

            `
            <div class="empty-history">

                🧾 No calculations yet.

                <br>

                Your calculations will
                appear here.

            </div>
            `;

        return;

    }


    /*
       Display every calculation.
    */

    history.forEach(
        function(item, index) {

            const historyItem =
                document.createElement(
                    "div"
                );


            historyItem.className =
                "history-item";


            /*
               Create expression.
            */

            const expression =
                document.createElement(
                    "div"
                );


            expression.className =
                "history-expression";


            expression.textContent =
                item.expression;


            /*
               Create result.
            */

            const result =
                document.createElement(
                    "div"
                );


            result.className =
                "history-result";


            result.textContent =
                "= " + item.result;


            /*
               Create time.
            */

            const time =
                document.createElement(
                    "div"
                );


            time.className =
                "history-time";


            time.textContent =
                item.time;


            /*
               Create action area.
            */

            const actions =
                document.createElement(
                    "div"
                );


            actions.className =
                "history-actions";


            /*
               Copy button.
            */

            const copyButton =
                document.createElement(
                    "button"
                );


            copyButton.type =
                "button";


            copyButton.textContent =
                "📋 Copy";


            copyButton.addEventListener(
                "click",
                function() {

                    copyHistoryResult(
                        index
                    );

                }
            );


            /*
               Delete button.
            */

            const deleteButton =
                document.createElement(
                    "button"
                );


            deleteButton.type =
                "button";


            deleteButton.textContent =
                "🗑️ Delete";


            deleteButton.addEventListener(
                "click",
                function() {

                    deleteHistoryItem(
                        index
                    );

                }
            );


            /*
               Put buttons inside
               action area.
            */

            actions.appendChild(
                copyButton
            );


            actions.appendChild(
                deleteButton
            );


            /*
               Put everything inside
               history item.
            */

            historyItem.appendChild(
                expression
            );


            historyItem.appendChild(
                result
            );


            historyItem.appendChild(
                time
            );


            historyItem.appendChild(
                actions
            );


            /*
               Put item into history list.
            */

            historyContainer.appendChild(
                historyItem
            );

        }
    );

}



/* ==================================================
   COPY HISTORY RESULT
================================================== */

function copyHistoryResult(index) {

    const history =
        getHistory();


    if (
        !history[index]
    ) {

        return;

    }


    const value =
        history[index].result;


    /*
       Modern clipboard.
    */

    if (
        navigator.clipboard &&
        window.isSecureContext
    ) {

        navigator.clipboard
            .writeText(value)
            .then(
                function() {

                    showHistoryMessage(
                        "✅ Result copied!"
                    );

                }
            )
            .catch(
                function() {

                    fallbackCopy(
                        value
                    );

                }
            );

    }

    else {

        fallbackCopy(
            value
        );

    }

}



/* ==================================================
   FALLBACK COPY
================================================== */

function fallbackCopy(value) {

    const textArea =
        document.createElement(
            "textarea"
        );


    textArea.value =
        value;


    textArea.style.position =
        "fixed";


    textArea.style.left =
        "-999999px";


    document.body.appendChild(
        textArea
    );


    textArea.focus();

    textArea.select();


    try {

        document.execCommand(
            "copy"
        );


        showHistoryMessage(
            "✅ Result copied!"
        );

    }

    catch (error) {

        showHistoryMessage(
            "❌ Unable to copy."
        );

    }


    document.body.removeChild(
        textArea
    );

}



/* ==================================================
   DELETE ONE HISTORY ITEM
================================================== */

function deleteHistoryItem(index) {

    const history =
        getHistory();


    if (
        index < 0 ||
        index >= history.length
    ) {

        return;

    }


    history.splice(
        index,
        1
    );


    saveHistory(
        history
    );


    displayHistory();

}



/* ==================================================
   CLEAR ALL HISTORY
================================================== */

function clearHistory() {

    const history =
        getHistory();


    /*
       Nothing to delete.
    */

    if (
        history.length === 0
    ) {

        return;

    }


    const confirmed =
        window.confirm(
            "Are you sure you want to clear all calculation history?"
        );


    if (!confirmed) {

        return;

    }


    localStorage.removeItem(
        HISTORY_KEY
    );


    displayHistory();


    showHistoryMessage(
        "🗑️ History cleared."
    );

}



/* ==================================================
   TEMPORARY MESSAGE
================================================== */

function showHistoryMessage(message) {

    /*
       Remove previous message.
    */

    const oldMessage =
        document.getElementById(
            "historyMessage"
        );


    if (oldMessage) {

        oldMessage.remove();

    }


    /*
       Create message.
    */

    const messageElement =
        document.createElement(
            "div"
        );


    messageElement.id =
        "historyMessage";


    messageElement.textContent =
        message;


    messageElement.style.position =
        "fixed";


    messageElement.style.bottom =
        "25px";


    messageElement.style.left =
        "50%";


    messageElement.style.transform =
        "translateX(-50%)";


    messageElement.style.padding =
        "12px 20px";


    messageElement.style.background =
        "#111827";


    messageElement.style.color =
        "white";


    messageElement.style.borderRadius =
        "8px";


    messageElement.style.zIndex =
        "9999";


    messageElement.style.fontSize =
        "14px";


    document.body.appendChild(
        messageElement
    );


    /*
       Remove after 2 seconds.
    */

    setTimeout(
        function() {

            if (
                messageElement
                .parentNode
            ) {

                messageElement.remove();

            }

        },
        2000
    );

}



/* ==================================================
   PAGE LOAD
================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        displayHistory();

    }
);