function retrieve_transaction_list() {
    $("#transactions").load("retrieve-transactions/", function () {
        // Callback function goes here (e.g. error handling)
    });
}

$(document).ready(function () {
    retrieve_transaction_list();
});