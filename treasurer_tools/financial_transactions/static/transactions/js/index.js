function convertDateToString(date) {
    var year = date.getFullYear();

    var month

    if (date.getMonth() < 9) {
        month = "0" + (date.getMonth() + 1);
    } else {
        month = date.getMonth() + 1;
    }

    var day;

    if (date.getDate() < 10) {
        day = "0" + (date.getDate());
    } else {
        day = date.getDate();
    }

    return year + "-" + month + "-" + day;
}

function setDefaultDates() {
    var today = new Date()
    var dateEnd = convertDateToString(today);
    var dateStart = convertDateToString(
        new Date(today.setDate(today.getDate() - 365))
    );

    $("#date-end").val(dateEnd);
    $("#date-start").val(dateStart);
}

function toggleDateInputs() {
    if ($("#transaction-dates").val() === "range") {
        $(".date").removeClass("hide");
    } else {
        $(".date").addClass("hide");
    }
}

function retrieveTransactions() {
    // Get the transaction type
    var transactionType = $("#transaction-type").val();

    // Get the start and stop dates
    var dateType = $("#transaction-dates").val();
    var today = new Date();
    var dateStart = "";
    var dateEnd = "";

    if (dateType === "30 days") {
        dateEnd = convertDateToString(today);
        dateStart = convertDateToString(
            new Date(today.setDate(today.getDate() - 30))
        );
    } else if (dateType === "90 days") {
        dateEnd = convertDateToString(today);
        dateStart = convertDateToString(
            new Date(today.setDate(today.getDate() - 90))
        );
    } else if (dateType === "1 year") {
        dateEnd = convertDateToString(today);
        dateStart = convertDateToString(
            new Date(today.setDate(today.getDate() - 365))
        );
    } else if (dateType === "2 years") {
        dateEnd = convertDateToString(today);
        dateStart = convertDateToString(
            new Date(today.setDate(today.getDate() - 730))
        );
    } else {
        dateStart = $("#date-start").val() ? $("#date-start").val() : "";
        dateEnd = $("#date-end").val() ? $("#date-end").val() : "";
    }
    
    var url = "retrieve-transactions/";
    var parameters = "?"
        + "transaction_type=" + encodeURIComponent(transactionType)
        + "&date_start=" + dateStart
        + "&date_end=" + dateEnd;

    $("#transactions").load(url + parameters, function () {
        // Callback function goes here (e.g. error handling)
    });
}

function filterResults() {
    var filterText = $("#text-filter").val().toUpperCase();

    // Hide all transactions
    var $transactions = $(".transaction");

    $transactions.addClass("hide");

    $transactions.each(function (transactionIndex, transaction) {
        var $transaction = $(transaction);

        // Check transaction name
        var transactionMemo = $transaction.attr("data-memo").toUpperCase();

        if (transactionMemo.indexOf(filterText) !== -1) {
            $transaction.removeClass("hide");
            return true;
        }

        // Check payee/payers
        var payeePayer = $transaction.attr("data-payee-payer").toUpperCase();

        if (payeePayer.indexOf(filterText) !== -1) {
            $transaction.removeClass("hide");
            return true;
        }

        // Check transaction total
        var transactionTotal = $transaction.attr("data-transaction-total").toUpperCase();

        if (transactionTotal.indexOf(filterText) !== -1) {
            $transaction.removeClass("hide");
            return true;
        }

        $transaction.find(".item").each(function (itemIndex, item) {
            $item = $(item);

            // Check item names
            var itemDescription = $item.attr("data-description").toUpperCase();

            if (itemDescription.indexOf(filterText) !== -1) {
                $transaction.removeClass("hide");
                return false;
            }

            // Check item amounts
            var itemAmount = $item.attr("data-amount").toUpperCase();

            if (itemAmount.indexOf(filterText) !== -1) {
                $transaction.removeClass("hide");
                return false;
            }

            // Check item GST
            var itemGST = $item.attr("data-gst").toUpperCase();

            if (itemGST.indexOf(filterText) !== -1) {
                $transaction.removeClass("hide");
                return false;
            }

            // Check item total
            var itemTotal = $item.attr("data-total").toUpperCase();

            if (itemTotal.indexOf(filterText) !== -1) {
                $transaction.removeClass("hide");
                return false;
            }

            // Check item accounting codes
            $item.find(".financial-code").each(function (codeIndex, code) {
                var $code = $(code);

                // Check the accounting code
                var codeCode = $code.attr("data-code").toUpperCase();

                if (codeCode.indexOf(filterText) !== -1) {
                    $transaction.removeClass("hide");
                    return false;
                }

                // Check the accounting code description

                // Check the accounting code
                var codeDescription = $code.attr("data-code-description").toUpperCase();

                if (codeDescription.indexOf(filterText) !== -1) {
                    $transaction.removeClass("hide");
                    return false;
                }
            });
        });
    });
}

$(document).ready(function () {

    $("#transaction-type").on("change", function () {
        retrieveTransactions();
    });

    $("#transaction-dates").on("change", function () {
        toggleDateInputs();
        retrieveTransactions();
    });

    $("#date-start").on("change", function () {
        retrieveTransactions();
    });

    $("#date-end").on("change", function () {
        retrieveTransactions();
    });

    $("#text-filter").on("keyup", function () {
        filterResults();
    });

    toggleDateInputs();
    setDefaultDates();
    retrieveTransactions();
});