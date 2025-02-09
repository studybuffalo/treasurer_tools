// Initialize raven monitoring
Raven.config('https://9399448340a14ab39198ade192bf8284@sentry.studybuffalo.com/2').install();

// Message functionality
function handleMessages(data, level = 20) {
  const $messageList = $('#messages');
  const $item = $('<li></li>');

  $item
    .text(data)
    .addClass(`level-${level}`)
    .appendTo($messageList);
}

// Convert number to currency string
function toCurrency(currencyNumber) {
  const currencyString = currencyNumber.toLocaleString(
    'en-CA',
    {
      style: 'currency',
      currency: 'CAD',
      currencyDisplay: 'symbol',
    },
  );

  return currencyString;
}
