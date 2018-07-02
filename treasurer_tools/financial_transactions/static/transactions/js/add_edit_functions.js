function update_financial_code(yearSelect) {
    // Shows only financial codes for the selected budget year
    const $yearSelect = $(yearSelect);
    const codeID = $yearSelect.attr("id").replace("budget_year", "code");
    const $codeSelect = $(`#${ codeID }`);
    const $codeGroups = $codeSelect.children();

    const yearID = $yearSelect.val();

    if (yearID) {
        // Cycle through each option group
        $codeGroups.each(function (groupIndex, optGroup) {
            let $optGroup = $(optGroup);

            // Cycle through each option under the group
            let $options = $optGroup.children();
            let visible_option = false;

            $options.each(function (optionIndex, option) {
                let $option = $(option);

                if ($option.attr("data-year_id") === yearID) {
                    $option.prop("hidden", false);
                    visible_option = true;
                } else {
                    $option.prop("hidden", true);
                }
            });

            // If there is any visible option, display the optgroup
            if (visible_option) {
                $optGroup.prop("hidden", false);
            } else {
                $optGroup.prop("hidden", true);
            }
        });
    }
}

function reset_financial_code(yearSelect) {
    const $fieldset = $(yearSelect).closest("fieldset");
    $fieldset.find('[id*="-code"]').val("");
}

function add_item() {
    // Get the current number of items
    var count = Number($("[id$=TOTAL_FORMS").val());

    // Get the template and replace it with the proper item ID
    var template = $("#item-template").html();
    var replacedTemplate = template.replace(/__prefix__/g, count);
    // Add the replaced template after the last formset-row
    $("#transaction-items").append(replacedTemplate);

    // Update the form count
    $("[id$=TOTAL_FORMS").val(count + 1);
}

function add_event_listeners_to_new_formset_row(e) {
    // Get the last formset row (i.e. the added row)
    const $lastRow = $(".formset-row:last");

    // Cycle through each budget year select
    $lastRow.find('[id*="-budget_year"]').each(function (index, select) {
        // Update the financial code select associated with this budget year
        update_financial_code(select);

        // Add required event listeners to the budget year
        $(select).on("click", function () {
            reset_financial_code(this);
            update_financial_code(this);
        });
    });

    // Cycle through each help button
    $lastRow.find("button.input-help").each(function (index, button) {
        $(button).on("click", function(e) {
            show_help_text(e, this);
        });
    });
}

$(document).ready(function () {
    $('[id*="-budget_year"]').on("change", function () {
        reset_financial_code(this);
        update_financial_code(this);
    });

    $("#add-item").on("click", function (e) {
        e.preventDefault();
        add_item();
        add_event_listeners_to_new_formset_row(e);
    });

    // Run an initial update on all selects
    $('[id*="-budget_year"]').each(function (index, select) {
        update_financial_code(select);
    });

    // Handles drag and drop attachment functionality
    $("#attachment-drop-zone").on("drop", function(e) {
        e.preventDefault();

        const attachmentInput = document.getElementById("id_newattachment-attachment_files");

        // Add files to the attachment input
        attachmentInput.files = e.originalEvent.dataTransfer.files;

        // Update the input to show the file
        attachmentInput.dispatchEvent(new Event('change'))
    });

    $("#attachment-drop-zone").on("dragover dragenter", function(e) {
        e.preventDefault();

        $("#attachment-drop-zone").addClass("is-dragover");
    });

    $("#attachment-drop-zone").on("dragleave dragend drop", function(e) {
        e.preventDefault();

        $("#attachment-drop-zone").removeClass("is-dragover");
    });
});
