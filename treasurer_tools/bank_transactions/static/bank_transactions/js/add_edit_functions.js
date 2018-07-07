function addItem() {
  // Get the current number of items
  const $totalForms = $('#id_banktransaction_set-TOTAL_FORMS');
  const count = Number($totalForms.val());

  // Get the template and replace it with the proper item ID
  const template = $('#item-template').html();
  const replacedTemplate = template.replace(/__prefix__/g, count);

  // Add the replaced template after the last formset-row
  $('#add-item').parent().before(replacedTemplate);

  // Update the form count
  $totalForms.val(count + 1);
}

function addEventListenersToNewFormsetRow(e) {
  // Get the last formset row (i.e. the added row)
  const $lastRow = $('.formset-row:last');

  // Cycle through each help button
  $lastRow.find('button.input-help').each((index, button) => {
    $(button).on('click', (e) => {
      show_help_text(e, this);
    });
  });
}

$(document).ready(() => {
  $('#add-item').on('click', (e) => {
    e.preventDefault();
    addItem();
    addEventListenersToNewFormsetRow(e);
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
