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

function createDateInputs(data) {
    var system_start = moment(data.system_year_start, "YYYY-MM-DD");
    var system_end = moment(data.system_year_end, "YYYY-MM-DD");
    var budget_years = data.budget_years

    // Create array of all the system years and months
    // TODO: Figure out how to handle months
    system_years = []
    system_months = []

    var system_year_start = system_start.year();
    var system_year_end = system_end.year();
    var system_month_start = system_start.month();
    var system_month_end = system_end.month();

    for (var i = 0; i < (system_year_end - system_year_start) + 2; i++) {
        year = system_year_start + i;
        system_years.push({
            start: moment({ year: year, month: 0, day: 1 }),
            end: moment({ year: year, month: 11, day: 31 })
        });
    }
    console.log(system_years);  
    console.log(budget_years);

    // Update the system year select
    var $systemYearSelect = $("#date-year-start");

    // Remove prior entries
    $systemYearSelect.children().remove

    $.each(system_years, function (index, year) {
        var $option = $("<option></option>")
        $option
            .text(year.start.toString("YYYY-MM-DD") + " to " + year.end)
            .attr("data-start", year.start)
            .attr("date-end", year.end);
        
        $systemYearSelect.append($option);
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
                createDateInputs(dateData);
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