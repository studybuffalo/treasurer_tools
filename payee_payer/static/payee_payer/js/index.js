function retrieve_payee_payer_list() {
    /*
    $.ajax({
        url: "retrieve-payee-payer-list/",
        type: "POST",
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader(
                    "X-CSRFToken",
                    $("[name=csrfmiddlewaretoken]").val()
                );
            }
        },
        success: function (results) {
            console.log(results);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error retrieving entries");
            console.error(textStatus + ": " + errorThrown);
        }
    });
    */
    $("#payee-payer-list").load("retrieve-payee-payer-list/", function () {
        console.log("loaded!");
    });
}

$(document).ready(function () {
    retrieve_payee_payer_list();
});