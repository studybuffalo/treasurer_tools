function updateProvinceInput(currentSelection = 'Alberta') {
  function createOptions(values) {
    // Converts an array of values into an array of option elements
    const options = [];

    $.each(values, (index, value) => {
      const $option = $('<option></option>');
      $option.val(value).text(value);
      options.push($option);
    });

    return options;
  }

  // Array of Canadian provinces
  const provinces = [
    'Alberta',
    'British Columbia',
    'Manitoba',
    'New Brunswick',
    'Newfoundland and Labrador',
    'Northwest Territories',
    'Nova Scotia',
    'Nunavut',
    'Ontario',
    'Prince Edward Island',
    'Quebec',
    'Saskatchewan',
    'Yukon',
  ];

  // Array of USA States
  const states = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming',
  ];

  // Get currenty country value
  const country = $('#id_country option:selected').text();

  let $newInput;

  // Create basic element
  if (country === 'Canada') {
    $newInput = $('<select></select>');
    $newInput.append(createOptions(provinces));
  } else if (country === 'United States') {
    $newInput = $('<select></select>');
    $newInput.append(createOptions(states));
  } else {
    $newInput = $('<input>');
    $newInput.attr('type', 'text');
  }

  // Add required properties
  $newInput
    .attr('name', 'province')
    .attr('maxlength', '100')
    .prop('required', true)
    .attr('id', 'id_province');

  // Remove the old input
  const $oldInput = $('#id_province');
  const $span = $oldInput.parent();

  $oldInput.remove();

  // Add the new input
  $span.append($newInput);

  // If provided, set the select to currentSelection
  $newInput.val(currentSelection);
}

function setCountryToCanada() {
  $('#id_country option:contains("Canada")').attr('selected', 'selected');
  updateProvinceInput();
}

$(document).ready(() => {
  // If not country provided, set to Canada
  if (document.getElementById('id_country').value === '') {
    setCountryToCanada();
  } else {
    const currentSelection = $('#id_province').val();
    updateProvinceInput(currentSelection);
  }

  $('#id_country').on('change', () => {
    updateProvinceInput();
  });
});
