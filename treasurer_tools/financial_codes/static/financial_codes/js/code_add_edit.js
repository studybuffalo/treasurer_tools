function updateFinancialCodeGroup() {
  const yearID = $('#id_budget_year').val();
  const $groupSelect = $('#id_financial_code_group');
  const $groupOptions = $groupSelect.children();

  if (yearID) {
    // Show code group options with data_system_id matching systemID
    $groupOptions.each((index, option) => {
      const $option = $(option);

      if ($option.attr('data-year_id') === yearID) {
        $option.prop('hidden', false);
      } else {
        $option.prop('hidden', true);
      }
    });

    // Enable the selects
    $groupSelect.prop('disabled', false);
  } else {
    // No system selected - disable group and year selects
    $groupSelect.prop('disabled', true);
  }
}

function resetGroupSelection() {
  $('#id_financial_code_group').val('');
}

$(document).ready(() => {
  $('#id_budget_year').on('change', () => {
    resetGroupSelection();
    updateFinancialCodeGroup();
  });

  updateFinancialCodeGroup();
});
