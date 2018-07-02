function textSearch($div, text) {
  const uText = text.toUpperCase();

  // Search against name
  const $name = $div.find('.name');
  if ($name.length && $name.attr('data-name').toUpperCase().includes(uText)) {
    return true;
  }

  // Get location reference
  const $location = $div.find('.location');
  if ($location.length) {
    // Search against city
    if ($location.attr('data-city').toUpperCase().includes(uText)) {
      return true;
    }

    // Search against province
    if ($location.attr('data-province').toUpperCase().includes(uText)) {
      return true;
    }

    // Search against country
    if ($location.attr('data-country').toUpperCase().includes(uText)) {
      return true;
    }
  }

  // Search against phone
  const $phone = $div.find('.phone');
  if ($phone.length && $phone.attr('data-phone').toUpperCase().includes(uText)) {
    return true;
  }

  // Search against fax
  const $fax = $div.find('.fax');
  if ($fax.length && $fax.attr('data-fax').toUpperCase().includes(uText)) {
    return true;
  }

  // Search against email
  const $email = $div.find('.email');
  if ($email.length && $email.attr('data-email').toUpperCase().includes(uText)) {
    return true;
  }

  return false;
}

function filterPayeePayerList() {
  const filterText = $('#filter-text').val();
  const filterStatus = $('#filter-status').val();

  const $payeePayers = $('#payee-payer-list > div');

  for (let i = 0; i < $payeePayers.length; i += 1) {
    let match = false;

    // Hide class first
    $payeePayers.eq(i).addClass('hide');

    // Filter by status
    if (filterStatus) {
      if ($payeePayers.eq(i).hasClass(filterStatus)) {
        if (filterText) {
          if (textSearch($payeePayers.eq(i), filterText)) {
            match = true;
          }
          // No text filter to apply
        } else {
          match = true;
        }
      }
    // All statuses being searched
    } else if (filterText) {
      if (textSearch($payeePayers.eq(i), filterText)) {
        match = true;
      }
      // No text filter to apply
    } else {
      match = true;
    }

    // Check for match
    if (match) {
      $payeePayers.eq(i).removeClass('hide');
    }
  }
}

function retrievePayeePayerList() {
  $('#payee-payer-list').load('retrieve-payee-payer-list/', () => {
    // Run filter
    filterPayeePayerList();
  });
}

$(document).ready(() => {
  retrievePayeePayerList();

  $('#filter-text').on('keyup change', () => {
    filterPayeePayerList();
  });

  $('#filter-status').on('change', () => {
    filterPayeePayerList();
  });
});
