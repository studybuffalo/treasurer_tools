function retrieve_payee_payer_list() {
    $("#payee-payer-list").load("retrieve-payee-payer-list/", function () {
        // Callback function goes here (e.g. error handling)
    });
}

$(document).ready(function () {
    retrieve_payee_payer_list();
});