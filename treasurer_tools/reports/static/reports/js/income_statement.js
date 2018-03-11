function updateDateInputs() {
    var predefined = $("#date-predefined").val();
    var today = moment();

    if (predefined === "last 30 days") {
        $("#date-end").val(today.format("YYYY-MM-DD"));
        $("#date-start").val(today.subtract(30, "days").format("YYYY-MM-DD"));
    } else if (predefined === "last year") {
        $("#date-end").val(today.format("YYYY-MM-DD"));
        $("#date-start").val(today.subtract(1, "years").format("YYYY-MM-DD"));
    } else if (predefined === "year-to-date") {
        $("#date-start").val(
            moment(today.year() + "-01-01").format("YYYY-MM-DD")
        );
        $("#date-end").val(today.format("YYYY-MM-DD"));
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
        + "&date_start=" + dateStart
        + "&date_end=" + dateEnd;

    $("#report").load(url + parameters, function () {
        // Callback function goes here (e.g. error handling)
    });
}

$(document).ready(function () {
    $("#financial-code-system").on("change", function () {
        retrieveReport();
    });

    $("#date-predefined").on("change", function () {
        updateDateInputs();
    });

    $("#date-start").on("change", function () {
        retrieveReport();
    });

    $("#date-end").on("change", function () {
        retrieveReport();
    });

    updateDateInputs();
    retrieveReport();
});