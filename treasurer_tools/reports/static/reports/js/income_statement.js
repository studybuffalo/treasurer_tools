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

function retrieveReport() {
  // Get the financial code system
  const financialCodeSystem = $('#financial-code-system').val();

  // Get the grouping type
  const grouping = $('#grouping').val();

  // Get the start and stop dates
  const dateStart = $('#date-start').val() ? $('#date-start').val() : '';
  const dateEnd = $('#date-end').val() ? $('#date-end').val() : '';

  const url = 'retrieve-report/';
  const parameters = `?
      financial_code_system=${financialCodeSystem}
      &date_start=${dateStart}
      &date_end=${dateEnd}`;

  $('#report').load(url + parameters, () => {
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
