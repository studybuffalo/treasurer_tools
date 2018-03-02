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

    toggleDateInputs();
    setDefaultDates();
    retrieveTransactions();
});