function handleMessages(data, error = false) {
  // Adds provided data to the message list
  const $messageList = $('#messages');
  const $item = $('<li></li>');
  $item
    .text(data)
    .appendTo($messageList);

  if (error) {
    $item.addClass('level_50');
  }
}

function updateTotals() {
  // Collect all the revenue transactions
  const $revenueTransactions = $('#revenue-accounts .transaction');
  const revenueLength = $revenueTransactions.length;
  let revenueTotal = 0;

  // Total all the values
  for (let i = 0; i < revenueLength; i += 1) {
    revenueTotal += Number($revenueTransactions.eq(i).attr('data-total'));
  }

  // Update the total display
  $('#revenue-total').text(`$${revenueTotal.toFixed(2)}`);

  // Collect all the expense transactions
  const $expenseTransactions = $('#expense-accounts .transaction');
  const expenseLength = $expenseTransactions.length;
  let expenseTotal = 0;

  // Total all the values
  for (let i = 0; i < expenseLength; i += 1) {
    const total = $expenseTransactions.eq(i).attr('data-total');

    if (total) {
      expenseTotal += Number(total);
    }
  }

  // Update the total display
  $('#expense-total').text(`$${expenseTotal.toFixed(2)}`);

  // Calculate the final net total
  const netTotal = revenueTotal - expenseTotal;

  // Update the display
  $('#net-total').text(`$${Math.abs(netTotal).toFixed(2)}`);

  // Add the negative class if necessary
  if (netTotal < 0) {
    $('#net-total').addClass('negative');
  } else {
    $('#net-total').removeClass('negative');
  }
}

function retrieveReport() {
  // Get the financial code system
  const budgetYear = $('#budget-year').val();

  if (budgetYear) {
    const url = 'retrieve-report/';
    const parameters = `?budget_year=${budgetYear}`;

    $('#report').load(url + parameters, (response, status, xhr) => {
      if (status === 'success') {
        updateTotals();
      } else if (status === 'error') {
        handleMessages(`${status.status} error: ${xhr.statusText}`, true);
      } else {
        handleMessages(`Error: ${response}`, true);
      }
    });
  }
}

$(document).ready(() => {
  $('#budget-year').on('change', () => {
    retrieveReport();
  });

  retrieveReport();
});
