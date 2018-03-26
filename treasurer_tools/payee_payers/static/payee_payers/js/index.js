function retrieve_payee_payer_list() {
    console.log("test")
    $("#payee-payer-list").load("retrieve-payee-payer-list/", function () {
        // Callback function goes here (e.g. error handling)
    });
}

$(document).ready(function () {
    retrieve_payee_payer_list();
});