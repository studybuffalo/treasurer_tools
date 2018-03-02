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

function retrieve_transactions() {
    // Get the transaction type
    var transactionType = $("#transaction-type").val();

    // Get the start and stop dates
    var dateType = $("#transaction-dates").val();
    var today = new Date();
    var dateStart;
    var dateEnd;

    if (dateType === "30 days") {
        dateStart = convertDateToString(today);
        dateEnd = convertDateToString(
            new Date(today.setDate(today.getDate() - 30))
        );
    } else if (dateType === "90 days") {
        dateStart = convertDateToString(today);
        dateEnd = convertDateToString(
            new Date(today.setDate(today.getDate() - 90))
        );
    } else if (dateType === "1 year") {
        dateStart = convertDateToString(today);
        dateEnd = convertDateToString(
            new Date(today.setDate(today.getDate() - 365))
        );
    } else if (dateType === "2 years") {
        dateStart = convertDateToString(today);
        dateEnd = convertDateToString(
            new Date(today.setDate(today.getDate() - 730))
        );
    } else {
        dateStart = $("#date-start").val();
        dateEnd = $("#date-end").val();
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
        retrieve_transactions();
    });

    $("#transaction-dates").on("change", function () {
        retrieve_transactions();
    });

    retrieve_transactions();
});