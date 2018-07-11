function updateBudgetYearSelect() {
  // Limits budget year selections to ones under this
  // financial code system
  const systemID = $('#financial-code-system').val();

  // Toggle hide class
  const $options = $('#budget-year option');
  $options.each((index, option) => {
    const $option = $(option);
    if ($option.attr('data-system-id') === systemID) {
      $option.removeClass('hide');
    } else {
      $option.addClass('hide');
    }
  });

  // Remove the hide class from the default value
  $options.eq(0).removeClass('hide');

  // Set value back to nothing
  $('#budget-year').val('');
}

function updateDateInputs() {
  const periodSelect = $('#reporting-period').val();

  // Toggle additional inputs for custom date range
  if (periodSelect === 'custom') {
    $('.date-range').removeClass('hide');
  } else {
    $('.date-range').addClass('hide');
  }

  // Toggle select input for budget year selection
  if (periodSelect === 'budget year') {
    $('#budget-year-div').removeClass('hide');
    $('#budget-year-div').removeClass('hide');
  } else {
    $('#budget-year-div').addClass('hide');
    $('#budget-year-div').addClass('hide');
  }
}

function updateTotals() {
  // Collect all the revenue transactions
  const $revenueTransactions = $('#revenue-accounts .transaction');
  const revenueLength = $revenueTransactions.length;
  let revenueTotal = 0;

  // Total all the values
  for (let i = 0; i < revenueLength; i += 1) {
    const lineTotal = Number($revenueTransactions.eq(i).attr('data-total'));
    revenueTotal += Number.isNaN(lineTotal) ? 0 : lineTotal;
  }

  // Update the total display
  $('#revenue-total').text(toCurrency(revenueTotal));

  // Collect all the expense transactions
  const $expenseTransactions = $('#expense-accounts .transaction');
  const expenseLength = $expenseTransactions.length;
  let expenseTotal = 0;

  // Total all the values
  for (let i = 0; i < expenseLength; i += 1) {
    const lineTotal = Number($expenseTransactions.eq(i).attr('data-total'));
    expenseTotal += Number.isNaN(lineTotal) ? 0 : lineTotal;
  }

  // Update the total display
  $('#expense-total').text(toCurrency(expenseTotal));

  // Calculate the final net total
  const netTotal = revenueTotal - expenseTotal;

  // Update the display
  $('#net-total').text(toCurrency(Math.abs(netTotal)));

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

  // Get the start and stop dates (if applicable)
  const reportingPeriod = $('#reporting-period').val();

  let dateStart = '';
  let dateEnd = '';
  const today = moment();

  if (reportingPeriod === 'last 30 days') {
    dateEnd = today.format('YYYY-MM-DD');
    dateStart = today.subtract(30, 'days').format('YYYY-MM-DD');
  } else if (reportingPeriod === 'last year') {
    dateEnd = today.format('YYYY-MM-DD');
    dateStart = today.subtract(1, 'years').format('YYYY-MM-DD');
  } else if (reportingPeriod === 'year-to-date') {
    dateEnd = today.format('YYYY-MM-DD');
    dateStart = moment(`${today.year()}-01-01`).format('YYYY-MM-DD');
  } else if (reportingPeriod === 'custom') {
    dateEnd = $('#date-end').val() ? $('#date-end').val() : '';
    dateStart = $('#date-start').val() ? $('#date-start').val() : '';
  }

  // Get the budet year (if applicable)
  let budgetYear = '';

  if (reportingPeriod === 'budget year') {
    budgetYear = $('#budget-year').val();
  }

  const url = 'retrieve-report/';

  // Set proper parameters
  let parameters = '';

  if (reportingPeriod === 'budget year') {
    parameters = `?financial_code_system=${financialCodeSystem}&budget_year=${budgetYear}`;
  } else {
    parameters = `?financial_code_system=${financialCodeSystem}&date_start=${dateStart}&date_end=${dateEnd}`;
  }


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

$(document).ready(() => {
  $('#financial-code-system').on('change', () => {
    updateBudgetYearSelect();
    retrieveReport();
  });

  $('#reporting-period').on('change', () => {
    updateDateInputs();
    retrieveReport();
  });

  $('#date-start').on('change', () => {
    retrieveReport();
  });

  $('#date-end').on('change', () => {
    retrieveReport();
  });

  $('#budget-year').on('change', () => {
    retrieveReport();
  });

  // Run initial setup functions
  updateBudgetYearSelect();
  updateDateInputs();
  retrieveReport();
});
