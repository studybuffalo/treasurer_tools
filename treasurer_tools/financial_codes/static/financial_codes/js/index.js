$(document).ready(() => {
  $('.financial-code-system').on('click', (e) => {
    $(e.currentTarget).toggleClass('opened');
  });

  $('.budget-year').on('click', (e) => {
    $(e.currentTarget).toggleClass('opened');
  });
});
