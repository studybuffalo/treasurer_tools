function populateReport(data) {
  function populateDiv(value, $div, subZeroClass) {
    if (value < 0) {
      $div
        .addClass(subZeroClass)
        .text(`-${Math.abs(value).toLocaleString(
          undefined,
          {
            style: 'currency',
            currency: 'USD',
            currencyDisplay: 'symbol',
          },
        )}`);
    } else {
      $div
        .removeClass(subZeroClass)
        .text(`${Math.abs(value).toLocaleString(
          undefined,
          {
            style: 'currency',
            currency: 'USD',
            currencyDisplay: 'symbol',
          },
        )}`);
    }
  }

  // Populate cash
  const $cashDiv = $('#assets-cash');
  populateDiv(data.cash, $cashDiv, 'negative');

  // Populate investments
  const $investmentsDiv = $('#assets-investments');
  populateDiv(data.investments, $investmentsDiv, 'negative');

  // Populate accounts receivable
  const $receivableDiv = $('#assets-accounts-receivable');
  populateDiv(data.accounts_receivable, $receivableDiv, 'negative');

  // Populate total assets
  const $assetsTotalDiv = $('#assets-total');
  populateDiv(data.assets_total, $assetsTotalDiv, 'negative');

  // Populate debt
  const $debtDiv = $('#liabilities-debt');
  populateDiv(data.debt, $debtDiv, 'positive');

  // Populate accounts payable
  const $payableDiv = $('#liabilities-accounts-payable');
  populateDiv(data.accounts_payable, $payableDiv, 'positive');

  // Populate total liabilities
  const $liabilitiesTotalDiv = $('#liabilities-total');
  populateDiv(data.liabilities_total, $liabilitiesTotalDiv, 'positive');
}

function retrieveReport() {
  // Get the financial code system
  const budgetYear = $('#budget-year').val();

  if (budgetYear) {
    $.ajax({
      url: 'retrieve-report/',
      method: 'GET',
      contentType: 'application/json',
      dataType: 'json',
      data: {
        budget_year: budgetYear,
      },
      success: (responseData) => {
        populateReport(responseData);
      },
      error: (jqXHR, status, error) => {
        handleMessages(`${status} ${error}`, 40);
      },
    });
  }
}

$(document).ready(() => {
  $('#budget-year').on('change', () => {
    retrieveReport();
  });

  retrieveReport();
});
