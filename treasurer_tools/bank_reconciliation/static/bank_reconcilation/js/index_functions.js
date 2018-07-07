function setInitialDates() {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() < 9 ? `0${today.getMonth() + 1}` : today.getMonth() + 1;
  const day = today.getDate() < 9 ? `0${today.getDate()}` : today.getDate();

  const startDate = `${year - 1}-${month}-${day}`;
  $('#financial-start-date').val(startDate);
  $('#bank-start-date').val(startDate);

  const endDate = `${year}-${month}-${day}`;
  $('#financial-end-date').val(endDate);
  $('#bank-end-date').val(endDate);
}

function toggleTransactionSelection(e) {
  const $li = $(e.currentTarget);
  $li.toggleClass('selected');
}

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

function addTransactions(data) {
  if (data.type === 'financial') {
    $.each(data.data, (index, transaction) => {
      const $date = $('<span></span>');
      $date
        .addClass('date')
        .text(transaction.date);

      const $type = $('<span></span>');
      $type
        .addClass('type')
        .text(transaction.type);

      const $description = $('<span></span>');
      $description
        .addClass('description')
        .text(transaction.description);

      const $amount = $('<span></span>');
      $amount
        .addClass('amount')
        .text(transaction.total);

      const $li = $('<li></li>');
      $li
        .addClass('financial-item')
        .attr('data-id', transaction.id)
        .on('click', toggleTransactionSelection)
        .append($date)
        .append($type)
        .append($description)
        .append($amount)
        .appendTo($('#financial-transactions'));

      if (transaction.reconciled) {
        $li.addClass('reconciled');
      }
    });
  } else if (data.type === 'bank') {
    $.each(data.data, (index, transaction) => {
      const $date = $('<span></span>');
      $date
        .addClass('date')
        .text(transaction.date);

      const $description = $('<span></span>');
      $description
        .addClass('description')
        .text(transaction.description);

      const $debit = $('<span></span>');
      $debit
        .addClass('debit')
        .addClass('negative')
        .text(transaction.debit);

      const $credit = $('<span></span>');
      $credit
        .addClass('credit')
        .text(transaction.credit);

      const $li = $('<li></li>');
      $li
        .attr('data-id', transaction.id)
        .addClass('bank-item')
        .on('click', toggleTransactionSelection)
        .append($date)
        .append($description)
        .append($debit)
        .append($credit)
        .appendTo($('#bank-transactions'));

      if (transaction.reconciled) {
        $li.addClass('reconciled');
      }
    });
  }
}

function retrieveTransactions(transactionType, startDate, endDate) {
  $.ajax({
    url: 'retrieve-transactions/',
    method: 'GET',
    contentType: 'application/json',
    dataType: 'json',
    data: {
      transaction_type: transactionType,
      date_start: startDate,
      date_end: endDate,
    },
    success: (responseData) => {
      addTransactions(responseData);
    },
    error: (jqXHR, status, error) => {
      handleMessages(`${status} ${error}`);
    },
  });
}

function clearTransactions(transactionType) {
  if (transactionType === 'financial') {
    $('#financial-transactions').empty();
  } else if (transactionType === 'bank') {
    $('#bank-transactions').empty();
  }
}

function updateReconciledFilter(e) {
  const $li = $(e.currentTarget);
  const $parentList = $li.closest('ul');
  const $allLi = $parentList.find('li');

  $allLi.removeClass('selected');
  $li.addClass('selected');

  let newClass = '';

  if ($li.text() === 'Unreconciled') {
    newClass = 'unreconciled';
  } else if ($li.text() === 'Reconciled') {
    newClass = 'reconciled';
  }

  const $transactionList = $parentList.next();
  $transactionList
    .removeClass()
    .addClass(newClass);
}

function matchTransactions() {
  // Get the selected financial transactions
  const $selectedFinancialTransactions = $('#financial-transactions li.selected');
  const financialIDs = [];

  $selectedFinancialTransactions.each((index, transaction) => {
    financialIDs.push($(transaction).attr('data-id'));
  });

  // Get the selected bank transactions
  const $selectedBankTransactions = $('#bank-transactions li.selected');
  const bankIDs = [];

  $selectedBankTransactions.each((index, transaction) => {
    bankIDs.push($(transaction).attr('data-id'));
  });

  // Setup post data
  const postData = {
    financial_ids: financialIDs,
    bank_ids: bankIDs,
  };

  // Setup CSRF token for POST
  const CSRF = $('[name=csrfmiddlewaretoken]').val();

  $.ajax({
    url: 'match-transactions/',
    method: 'POST',
    dataType: 'json',
    data: JSON.stringify(postData),
    beforeSend: (xhr) => {
      if (!this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', CSRF);
      }
    },
    success: () => {
      handleMessages('Transactions matched');
    },
    error: (jqXHR, status, error) => {
      handleMessages(`${status} ${error}`, true);
    },
  });
}

function unmatchTransactions() {
  // Get the selected financial transactions
  const $selectedFinancialTransactions = $('#financial-transactions li.selected');
  const financialIDs = [];

  $selectedFinancialTransactions.each((index, transaction) => {
    financialIDs.push($(transaction).attr('data-id'));
  });

  // Get the selected bank transactions
  const $selectedBankTransactions = $('#bank-transactions li.selected');
  const bankIDs = [];

  $selectedBankTransactions.each((index, transaction) => {
    bankIDs.push($(transaction).attr('data-id'));
  });

  // Setup post data
  const postData = {
    financial_ids: financialIDs,
    bank_ids: bankIDs,
  };

  // Setup CSRF token for POST
  const CSRF = $('[name=csrfmiddlewaretoken]').val();

  $.ajax({
    url: 'unmatch-transactions/',
    method: 'POST',
    dataType: 'json',
    data: JSON.stringify(postData),
    beforeSend: (xhr) => {
      if (!this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', CSRF);
      }
    },
    success: () => {
      handleMessages('Transactions unmatched');
    },
    error: (jqXHR, status, error) => {
      handleMessages(`${status} ${error}`, true);
    },
  });
}

$(document).ready(() => {
  setInitialDates();

  $('#financial-update').on('click', () => {
    clearTransactions('financial');
    retrieveTransactions(
      'financial',
      $('#financial-start-date').val(),
      $('#financial-end-date').val(),
    );
  });

  $('#bank-update').on('click', () => {
    clearTransactions('bank');
    retrieveTransactions(
      'bank',
      $('#bank-start-date').val(),
      $('#bank-end-date').val(),
    );
  });

  $('#financial-reconciled-filter li, #bank-reconciled-filter li').on(
    'click', updateReconciledFilter,
  );

  $('#match').on('click', () => {
    matchTransactions();
  });

  $('#unmatch').on('click', () => {
    unmatchTransactions();
  });

  retrieveTransactions(
    'financial',
    $('#financial-start-date').val(),
    $('#financial-end-date').val(),
  );

  retrieveTransactions(
    'bank',
    $('#bank-start-date').val(),
    $('#bank-end-date').val(),
  );
});
