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
    var grouping = $("#grouping").val()

    if (grouping === "year") {

    } else if (grouping === "budget") {

    } else if (grouping === "month") {

    } else if (grouping === "week") {

    }
}

function retrieveReport() {
    // Get the financial code system
    var financialCodeSystem = $("#financial-code-system").val();

    // Get the grouping type
    grouping = $("#grouping").val();

    // Get the start and stop dates
    var dateStart = $("#date-start").val() ? $("#date-start").val() : "";
    var dateEnd = $("#date-end").val() ? $("#date-end").val() : "";

    var url = "retrieve-report/";
    var parameters = "?"
        + "financial_code_system=" + financialCodeSystem
        + "&grouping=" + grouping
        + "&date_start=" + dateStart
        + "&date_end=" + dateEnd;

    $("#report").load(url + parameters, function () {
        // Callback function goes here (e.g. error handling)
    });
}

function updateDateInputs() {
    /* Updates the date inputs with the proper values for the
     * financial code system
     */
    financial_code_system = $("#financial-code-system").val();

    $.ajax(
        "retrieve-dates/",
        {
            data: {financial_code_system: financial_code_system},
            dataType: "json",
            success: function (dateData) {
                console.log(dateData);
            },
            error: function (jqXHR, textStatus, error) {
                console.error(textStatus + ": " + error);
            }
        }
    );
}

$(document).ready(function () {
    $("#financial-code-system").on("change", function () {
        updateDateInputs();
        retrieveReport();
    });

    $("#grouping").on("change", function () {
        retrieveReport();
        toggleDateInputs();
    });

    $("#date-start").on("change", function () {
        retrieveReport();
    });

    $("#date-end").on("change", function () {
        retrieveReport();
    });
    
    toggleDateInputs();
    setDefaultDates();
    retrieveReport();
});