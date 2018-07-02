function convertDateToString(date) {
  const year = date.getFullYear();

  let month;

  if (date.getMonth() < 9) {
    month = `0${date.getMonth() + 1}`;
  } else {
    month = date.getMonth() + 1;
  }

  let day;

  if (date.getDate() < 10) {
    day = `0${date.getDate()}`;
  } else {
    day = date.getDate();
  }

  return `${year}-${month}-${day}`;
}

function setDefaultDates() {
  const today = new Date();
  const dateEnd = convertDateToString(today);
  const dateStart = convertDateToString(
    new Date(today.setDate(today.getDate() - 365)),
  );

  $('#date-end').val(dateEnd);
  $('#date-start').val(dateStart);
}

function toggleDateInputs() {
  if ($('#transaction-dates').val() === 'range') {
    $('.date').removeClass('hide');
  } else {
    $('.date').addClass('hide');
  }
}

function retrieveTransactions() {
  // Get the transaction type
  const transactionType = $('#transaction-type').val();

  // Get the start and stop dates
  const dateType = $('#transaction-dates').val();
  const today = new Date();
  let dateStart = '';
  let dateEnd = '';

  if (dateType === '30 days') {
    dateEnd = convertDateToString(
      new Date(today.setDate(today.getDate() + 1)),
    );
    dateStart = convertDateToString(
      new Date(today.setDate(today.getDate() - 30)),
    );
  } else if (dateType === '90 days') {
    dateEnd = convertDateToString(
      new Date(today.setDate(today.getDate() + 1)),
    );
    dateStart = convertDateToString(
      new Date(today.setDate(today.getDate() - 90)),
    );
  } else if (dateType === '1 year') {
    dateEnd = convertDateToString(
      new Date(today.setDate(today.getDate() + 1)),
    );
    dateStart = convertDateToString(
      new Date(today.setDate(today.getDate() - 365)),
    );
  } else if (dateType === '2 years') {
    dateEnd = convertDateToString(
      new Date(today.setDate(today.getDate() + 1)),
    );
    dateStart = convertDateToString(
      new Date(today.setDate(today.getDate() - 730)),
    );
  } else {
    dateStart = $('#date-start').val() ? $('#date-start').val() : '';
    dateEnd = $('#date-end').val() ? $('#date-end').val() : '';
  }

  const url = 'retrieve-transactions/';
  const parameters = '?'
      + `transaction_type=${encodeURIComponent(transactionType)}`
      + `&date_start=${dateStart}`
      + `&date_end=${dateEnd}`;

  $('#transactions').load(url + parameters, () => {
    // Callback function goes here (e.g. error handling)
  });
}

function filterResults() {
  const filterText = $('#text-filter').val().toUpperCase();

  // Hide all transactions
  const $transactions = $('.transaction');

  $transactions.addClass('hide');

  $transactions.each((transactionIndex, transaction) => {
    const $transaction = $(transaction);

    // Check transaction name
    const transactionMemo = $transaction.attr('data-memo').toUpperCase();

    if (transactionMemo.indexOf(filterText) !== -1) {
      $transaction.removeClass('hide');
      return false;
    }

    // Check payee/payers
    const payeePayer = $transaction.attr('data-payee-payer').toUpperCase();

    if (payeePayer.indexOf(filterText) !== -1) {
      $transaction.removeClass('hide');
      return false;
    }

    // Check transaction total
    const transactionTotal = $transaction.attr('data-transaction-total').toUpperCase();

    if (transactionTotal.indexOf(filterText) !== -1) {
      $transaction.removeClass('hide');
      return false;
    }

    $transaction.find('.item').each((itemIndex, item) => {
      const $item = $(item);

      // Check item names
      const itemDescription = $item.attr('data-description').toUpperCase();

      if (itemDescription.indexOf(filterText) !== -1) {
        $transaction.removeClass('hide');
        return false;
      }

      // Check item amounts
      const itemAmount = $item.attr('data-amount').toUpperCase();

      if (itemAmount.indexOf(filterText) !== -1) {
        $transaction.removeClass('hide');
        return false;
      }

      // Check item GST
      const itemGST = $item.attr('data-gst').toUpperCase();

      if (itemGST.indexOf(filterText) !== -1) {
        $transaction.removeClass('hide');
        return false;
      }

      // Check item total
      const itemTotal = $item.attr('data-total').toUpperCase();

      if (itemTotal.indexOf(filterText) !== -1) {
        $transaction.removeClass('hide');
        return false;
      }

      // Check item accounting codes
      $item.find('.financial-code').each((codeIndex, code) => {
        const $code = $(code);

        // Check the accounting code
        const codeCode = $code.attr('data-code').toUpperCase();

        if (codeCode.indexOf(filterText) !== -1) {
          $transaction.removeClass('hide');
          return false;
        }

        // Check the accounting code description

        // Check the accounting code
        const codeDescription = $code.attr('data-code-description').toUpperCase();

        if (codeDescription.indexOf(filterText) !== -1) {
          $transaction.removeClass('hide');
          return false;
        }

        return true;
      });

      return true;
    });

    return true;
  });
}

$(document).ready(() => {
  $('#transaction-type').on('change', () => {
    retrieveTransactions();
  });

  $('#transaction-dates').on('change', () => {
    toggleDateInputs();
    retrieveTransactions();
  });

  $('#date-start').on('change', () => {
    retrieveTransactions();
  });

  $('#date-end').on('change', () => {
    retrieveTransactions();
  });

  $('#text-filter').on('keyup', () => {
    filterResults();
  });

  toggleDateInputs();
  setDefaultDates();
  retrieveTransactions();
});
