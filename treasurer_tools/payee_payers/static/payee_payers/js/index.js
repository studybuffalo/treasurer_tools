function retrievePayeePayerList() {
  $('#payee-payer-list').load('retrieve-payee-payer-list/', () => {
    // Callback function goes here (e.g. error handling)
  });
}

$(document).ready(() => {
  retrievePayeePayerList();
});
