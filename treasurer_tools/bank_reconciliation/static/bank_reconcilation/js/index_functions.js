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

function toggleReconciledStatus(clickedButton) {
  if (clickedButton.id === 'button-reconcile-transactions') {
    $('#button-reconcile-transactions').addClass('selected');
    $('#button-show-reconciled-transactions').removeClass('selected');
  } else if (clickedButton.id === 'button-show-reconciled-transactions') {
    $('#button-reconcile-transactions').removeClass('selected');
    $('#button-show-reconciled-transactions').addClass('selected');
  }
}

function updateReconciledView() {
  if ($('#button-reconcile-transactions').hasClass('selected')) {
    $('.reconcile-div').removeClass('hide');
    $('.unreconcile-div').addClass('hide');
  } else {
    $('.reconcile-div').addClass('hide');
    $('.unreconcile-div').removeClass('hide');
  }
}

function toggleTransactionSelection($li) {
  $li.toggleClass('selected');
}

function checkForSelectionMismatch() {
  // Error Check List
  const errors = {
    mismatchExpenseRevenue: false,
    mismatchDebitCredit: false,
    mismatchExpenseCredit: false,
    mismatchRevenueDebit: false,
  };

  // Get all selected financial transactions
  const $financialTransactions = $('#financial-transactions .selected');
  const financialLength = $financialTransactions.length;

  // Get all selected bank transactions
  const $bankTransactions = $('#bank-transactions .selected');
  const bankLength = $bankTransactions.length;

  // Check if both expense and revenue are selected
  for (let i = 0; i < financialLength; i += 1) {
    for (let j = 1; j < financialLength; j += 1) {
      const type1 = $financialTransactions.eq(i).attr('data-type');
      const type2 = $financialTransactions.eq(j).attr('data-type');

      if (type1 !== type2) {
        errors.mismatchExpenseRevenue = true;
      }
    }
  }

  // Check if both debit and credit are selected
  for (let i = 0; i < bankLength; i += 1) {
    for (let j = 1; j < bankLength; j += 1) {
      const debit1 = $bankTransactions.eq(i).attr('data-amount-debit');
      const credit1 = $bankTransactions.eq(i).attr('data-amount-credit');
      const debit2 = $bankTransactions.eq(j).attr('data-amount-debit');
      const credit2 = $bankTransactions.eq(j).attr('data-amount-credit');

      if ((debit1 > 0 && credit2 > 0) || (credit1 > 0 && debit2 > 0)) {
        errors.mismatchDebitCredit = true;
      }
    }
  }

  // Check if expense and credit OR revenue and debit are selected
  for (let i = 0; i < financialLength; i += 1) {
    for (let j = 0; j < bankLength; j += 1) {
      const type = $financialTransactions.eq(i).attr('data-type');
      const debit = $bankTransactions.eq(j).attr('data-amount-debit');
      const credit = $bankTransactions.eq(j).attr('data-amount-credit');

      if (type === 'EXPENSE' && credit > 0) {
        errors.mismatchExpenseCredit = true;
      } else if (type === 'REVENUE' && debit > 0) {
        errors.mismatchRevenueDebit = true;
      }
    }
  }

  // Clear the error message list
  const $messages = $('#messages');
  $messages.empty();

  // Add warning messages
  if (errors.mismatchExpenseRevenue) {
    $messages.append(
      $('<li></li>')
        .addClass('level_30')
        .text('Warning: you have both expense and revenue financial transactions selected.'),
    );
  }

  if (errors.mismatchDebitCredit) {
    $messages.append(
      $('<li></li>')
        .addClass('level_30')
        .text('Warning: you have both debit and credit banking transactions selected.'),
    );
  }

  if (errors.mismatchExpenseCredit) {
    $messages.append(
      $('<li></li>')
        .addClass('level_30')
        .text('Warning: you have both expense financial transactions and credit bank transactions selected.'),
    );
  }

  if (errors.mismatchRevenueDebit) {
    $messages.append(
      $('<li></li>')
        .addClass('level_30')
        .text('Warning: you have both revenue financial transactions and debit bank transactions selected.'),
    );
  }
}

function updateTotal() {
  // Get all selected financial transaction
  const $financialTransactions = $('#financial-transactions .selected');
  const financialLength = $financialTransactions.length;

  // Get all selected bank transactions
  const $bankTransactions = $('#bank-transactions .selected');
  const bankLength = $bankTransactions.length;

  // Get the financial total
  let financialTotal = 0;

  for (let i = 0; i < financialLength; i += 1) {
    if ($financialTransactions.attr('data-type') === 'EXPENSE') {
      financialTotal -= Number($financialTransactions.eq(i).attr('data-total'));
    } else {
      financialTotal += Number($financialTransactions.eq(i).attr('data-total'));
    }
  }

  // Get the banking total
  let bankTotal = 0;

  for (let i = 0; i < bankLength; i += 1) {
    if (Number($bankTransactions.eq(i).attr('data-amount-debit')) > 0) {
      bankTotal -= Number($bankTransactions.eq(i).attr('data-amount-debit'));
    } else {
      bankTotal += Number($bankTransactions.eq(i).attr('data-amount-credit'));
    }
  }

  // Get the discrepancy
  const discrepancy = financialTotal - bankTotal;

  // Update the financial total display
  const financialTotalString = (financialTotal >= 0
    ? `$${financialTotal.toFixed(2)}`
    : `-$${Math.abs(financialTotal).toFixed(2)}`
  );
  $('#financial-total').text(financialTotalString);

  // Update the banking total display
  const bankTotalString = (bankTotal >= 0
    ? `$${bankTotal.toFixed(2)}`
    : `-$${Math.abs(bankTotal).toFixed(2)}`
  );
  $('#banking-total').text(bankTotalString);

  // Update the discrepancy display
  const discrepancyTotal = (discrepancy >= 0
    ? `$${discrepancy.toFixed(2)}`
    : `-$${Math.abs(discrepancy).toFixed(2)}`
  );
  $('#discrepancy').text(discrepancyTotal);

  if (discrepancy !== 0) {
    $('#discrepancy').addClass('negative');
  } else {
    $('#discrepancy').removeClass('negative');
  }
}

function handleTransactionClick(e) {
  // Get the clicked list element
  const $li = $(e.currentTarget);

  // Update the toggle class
  toggleTransactionSelection($li);

  // Check for selection mismatches
  checkForSelectionMismatch();

  // Update totals
  updateTotal();
}

function addTransactions(data) {
  if (data.type === 'financial') {
    // Clear any data already in list
    $('#financial-transactions').empty();

    $.each(data.data, (index, transaction) => {
      // Add transaction date
      const $dateDiv = $('<div></div>');
      $dateDiv.addClass('date');

      const $dateEm = $('<em></em>');
      $dateEm
        .text('Date: ')
        .appendTo($dateDiv);

      const $date = $('<span></span>');
      $date
        .text(transaction.date)
        .appendTo($dateDiv);

      // Add type
      const $typeDiv = $('<div></div>');
      $typeDiv.addClass('type');

      const $typeEm = $('<em></em>');
      $typeEm
        .text('Type: ')
        .appendTo($typeDiv);

      const $type = $('<span></span>');
      $type
        .text(transaction.type)
        .appendTo($typeDiv);

      // Add description
      const $descriptionDiv = $('<div></div>');
      $descriptionDiv.addClass('description');

      const $descriptionEm = $('<em></em>');
      $descriptionEm
        .text('Description: ')
        .appendTo($descriptionDiv);

      const $description = $('<span></span>');
      $description
        .text(transaction.description)
        .appendTo($descriptionDiv);

      // Add amount
      const $amountDiv = $('<div></div>');
      $amountDiv.addClass('amount');

      const $amountEm = $('<em></em>');
      $amountEm
        .text('Amount: ')
        .appendTo($amountDiv);

      const $amount = $('<span></span>');
      $amount
        .text(`$${transaction.total}`)
        .appendTo($amountDiv);

      if (transaction.type.toUpperCase() === 'EXPENSE') {
        $amount.addClass('negative');
      }

      const $li = $('<li></li>');
      $li
        .addClass('financial-item')
        .attr('data-id', transaction.id)
        .attr('data-type', transaction.type.toUpperCase())
        .attr('data-total', transaction.total)
        .attr('data-date', transaction.date)
        .attr('data-description', transaction.description.toUpperCase())
        .attr('data-amount', transaction.total)
        .on('click', handleTransactionClick)
        .append($dateDiv)
        .append($typeDiv)
        .append($descriptionDiv)
        .append($amountDiv)
        .appendTo($('#financial-transactions'));

      if (transaction.reconciled) {
        $li.addClass('reconciled');
      }
    });
  } else if (data.type === 'bank') {
    // Clear any data already in list
    $('#bank-transactions').empty();

    $.each(data.data, (index, transaction) => {
      // Add transaction date
      const $dateDiv = $('<div></div>');
      $dateDiv.addClass('date');

      const $dateEm = $('<em></em>');
      $dateEm
        .text('Date: ')
        .appendTo($dateDiv);

      const $date = $('<span></span>');
      $date
        .text(transaction.date)
        .appendTo($dateDiv);

      // Add description
      const $descriptionDiv = $('<div></div>');
      $descriptionDiv.addClass('description');

      const $descriptionEm = $('<em></em>');
      $descriptionEm
        .text('Description: ')
        .appendTo($descriptionDiv);

      const $description = $('<span></span>');
      $description
        .text(transaction.description)
        .appendTo($descriptionDiv);

      // Add debit
      const $debitDiv = $('<div></div>');
      $debitDiv.addClass('debit');

      const $debitEm = $('<em></em>');
      $debitEm
        .text('Debit: ')
        .appendTo($debitDiv);

      const $debit = $('<span></span>');
      $debit
        .text(`$${transaction.debit}`)
        .appendTo($debitDiv);

      if (transaction.debit > 0) {
        $debit.addClass('negative');
      }

      // Add credit
      const $creditDiv = $('<div></div>');
      $creditDiv.addClass('credit');

      const $creditEm = $('<em></em>');
      $creditEm
        .text('Credit: ')
        .appendTo($creditDiv);

      const $credit = $('<span></span>');
      $credit
        .text(`$${transaction.credit}`)
        .appendTo($creditDiv);

      const $li = $('<li></li>');
      $li
        .attr('data-id', transaction.id)
        .attr('data-amount-debit', transaction.debit)
        .attr('data-amount-credit', transaction.credit)
        .attr('data-date', transaction.date)
        .attr('data-description', transaction.description.toUpperCase())
        .attr('data-amount', `${transaction.debit} ${transaction.credit}`)
        .addClass('bank-item')
        .on('click', handleTransactionClick)
        .append($dateDiv)
        .append($descriptionDiv)
        .append($debitDiv)
        .append($creditDiv)
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

function updateReconciledFilter(e, $transactionList) {
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

  $transactionList
    .removeClass('unreconciled reconciled')
    .addClass(newClass);
}

function filterResults(input, $list) {
  // Get the text to filter against
  const filterText = $(input.target).val().toUpperCase();

  // Get the list items to search through
  const $items = $list.find('.financial-item, .bank-item');

  $items.each((index, item) => {
    const $item = $(item);

    // Hide the item by default
    $item.addClass('hide');

    // Check the values to compare
    const itemDate = $item.attr('data-date');
    const itemDescription = $item.attr('data-description');
    const itemAmount = $item.attr('data-amount');

    // Check if there are any matches
    if (
      itemDate.indexOf(filterText) !== -1
      || itemDescription.indexOf(filterText) !== -1
      || itemAmount.indexOf(filterText) !== -1
    ) {
      $item.removeClass('hide');
    }

    return true;
  });
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

      // Add reconciled filters to each item
      $selectedFinancialTransactions.addClass('reconciled');
      $selectedBankTransactions.addClass('reconciled');

      // Remove the selected filter
      $selectedFinancialTransactions.removeClass('selected');
      $selectedBankTransactions.removeClass('selected');

      // Update the totals and update messages
      checkForSelectionMismatch();
      updateTotal();
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

      // Remove the reconciled filter
      $selectedFinancialTransactions.removeClass('reconciled');
      $selectedBankTransactions.removeClass('reconciled');

      // Remove the selected filter
      $selectedFinancialTransactions.removeClass('selected');
      $selectedBankTransactions.removeClass('selected');

      // Update the totals and update messages
      checkForSelectionMismatch();
      updateTotal();
    },
    error: (jqXHR, status, error) => {
      handleMessages(`${status} ${error}`, true);
    },
  });
}

$(document).ready(() => {
  setInitialDates();

  $('#reconciled-status-buttons').on('click', (e) => {
    toggleReconciledStatus(e.target);
    updateReconciledView();
  });

  $('#financial-start-date').on('change', () => {
    clearTransactions('financial');
    retrieveTransactions(
      'financial',
      $('#financial-start-date').val(),
      $('#financial-end-date').val(),
    );
  });

  $('#financial-end-date').on('change', () => {
    clearTransactions('financial');
    retrieveTransactions(
      'financial',
      $('#financial-start-date').val(),
      $('#financial-end-date').val(),
    );
  });

  $('#bank-start-date').on('change', () => {
    clearTransactions('bank');
    retrieveTransactions(
      'bank',
      $('#bank-start-date').val(),
      $('#bank-end-date').val(),
    );
  });

  $('#bank-end-date').on('change', () => {
    clearTransactions('bank');
    retrieveTransactions(
      'bank',
      $('#bank-start-date').val(),
      $('#bank-end-date').val(),
    );
  });

  $('#financial-text-filter').on('keyup', (e) => {
    filterResults(e, $('#financial-transactions'));
  });

  $('#bank-text-filter').on('keyup', (e) => {
    filterResults(e, $('#bank-transactions'));
  });

  $('#financial-reconciled-filter li').on('click', (e) => {
    updateReconciledFilter(e, $('#financial-transactions'));
  });

  $('#bank-reconciled-filter li').on('click', (e) => {
    updateReconciledFilter(e, $('#bank-transactions'));
  });

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

  // Run initial total calculation
  updateTotal();
});
