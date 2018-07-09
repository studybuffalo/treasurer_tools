function updateFinancialCode(yearSelect) {
  // Shows only financial codes for the selected budget year
  const $yearSelect = $(yearSelect);
  const codeID = $yearSelect.attr('id').replace('budget_year', 'code');
  const $codeSelect = $(`#${codeID}`);
  const $codeGroups = $codeSelect.children();

  const yearID = $yearSelect.val();

  if (yearID) {
    // Cycle through each option group
    $codeGroups.each((groupIndex, optGroup) => {
      const $optGroup = $(optGroup);

      // Cycle through each option under the group
      const $options = $optGroup.children();
      let visibleOption = false;

      $options.each((optionIndex, option) => {
        const $option = $(option);

        if ($option.attr('data-year_id') === yearID) {
          $option.prop('hidden', false);
          visibleOption = true;
        } else {
          $option.prop('hidden', true);
        }
      });

      // If there is any visible option, display the optgroup
      if (visibleOption) {
        $optGroup.prop('hidden', false);
      } else {
        $optGroup.prop('hidden', true);
      }
    });
  }
}

function resetFinancialCode(yearSelect) {
  const $yearSelect = $(yearSelect);
  const codeID = $yearSelect.attr('id').replace('budget_year', 'code');
  const $codeSelect = $(`#${codeID}`);

  $codeSelect.val('');
}

function addItem() {
  // Get the current number of items
  const count = Number($('[id$=TOTAL_FORMS').val());

  // Get the template and replace it with the proper item ID
  const template = $('#item-template').html();
  const replacedTemplate = template.replace(/__prefix__/g, count);

  // Add the replaced template after the last formset-row
  $('#transaction-items').append(replacedTemplate);

  // Update the form count
  $('[id$=TOTAL_FORMS').val(count + 1);
}

function addEventListenersToNewFormsetRow() {
  // Get the last formset row (i.e. the added row)
  const $lastRow = $('.transaction-item:last');

  // Cycle through each budget year select
  $lastRow.find('[id*="-budget_year"]').each((index, select) => {
    // Update the financial code select associated with this budget year
    updateFinancialCode(select);

    // Add required event listeners to the budget year
    $(select).on('change', (e) => {
      resetFinancialCode(e.currentTarget);
      updateFinancialCode(e.currentTarget);
    });
  });
}

$(document).ready(() => {
  $('[id*="-budget_year"]').on('change', (e) => {
    resetFinancialCode(e.currentTarget);
    updateFinancialCode(e.currentTarget);
  });

  $('#add-item').on('click', (e) => {
    e.preventDefault();
    addItem();
    addEventListenersToNewFormsetRow(e);
  });

  // Run an initial update on all selects
  $('[id*="-budget_year"]').each((index, select) => {
    updateFinancialCode(select);
  });

  // Handles drag and drop attachment functionality
  $('#attachment-drop-zone').on('drop', (e) => {
    e.preventDefault();

    const attachmentInput = document.getElementById('id_newattachment-attachment_files');

    // Add files to the attachment input
    attachmentInput.files = e.originalEvent.dataTransfer.files;

    // Update the input to show the file
    attachmentInput.dispatchEvent(new Event('change'));
  });

  $('#attachment-drop-zone').on('dragover dragenter', (e) => {
    e.preventDefault();

    $('#attachment-drop-zone').addClass('is-dragover');
  });

  $('#attachment-drop-zone').on('dragleave dragend drop', (e) => {
    e.preventDefault();

    $('#attachment-drop-zone').removeClass('is-dragover');
  });
});
