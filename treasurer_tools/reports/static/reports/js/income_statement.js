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

function updateDateInputs() {
  const predefined = $('#date-predefined').val();
  const today = moment();

  if (predefined === 'last 30 days') {
    $('#date-end').val(today.format('YYYY-MM-DD'));
    $('#date-start').val(today.subtract(30, 'days').format('YYYY-MM-DD'));
  } else if (predefined === 'last year') {
    $('#date-end').val(today.format('YYYY-MM-DD'));
    $('#date-start').val(today.subtract(1, 'years').format('YYYY-MM-DD'));
  } else if (predefined === 'year-to-date') {
    $('#date-start').val(moment(`${today.year()}-01-01`).format('YYYY-MM-DD'));
    $('#date-end').val(today.format('YYYY-MM-DD'));
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
  const financialCodeSystem = $('#financial-code-system').val();

  // Get the grouping type
  // const grouping = $('#grouping').val();

  // Get the start and stop dates
  const dateStart = $('#date-start').val() ? $('#date-start').val() : '';
  const dateEnd = $('#date-end').val() ? $('#date-end').val() : '';

  const url = 'retrieve-report/';
  const parameters = `?financial_code_system=${financialCodeSystem}&date_start=${dateStart}&date_end=${dateEnd}`;

  $('#report').load(url + parameters, (response, status, xhr) => {
    if (status === 'success') {
      updateTotals();
    } else if (status === 'error') {
      handleMessages(`${status.status} error: ${xhr.statusText}`, true);
    } else {
      handleMessages(`Error: ${response}`, true);
    }
    // Callback function goes here (e.g. error handling)
  });
}

function updatePredefinedSelect() {
  /*
   * Changes the predefined select to custom when date input changed
   */

  $('#date-predefined').val('custom');
}

$(document).ready(() => {
  $('#financial-code-system').on('change', () => {
    retrieveReport();
  });

  $('#date-predefined').on('change', () => {
    updateDateInputs();
    retrieveReport();
  });

  $('#date-start').on('change', () => {
    updatePredefinedSelect();
    retrieveReport();
  });

  $('#date-end').on('change', () => {
    updatePredefinedSelect();
    retrieveReport();
  });

  updateDateInputs();
  retrieveReport();
});
