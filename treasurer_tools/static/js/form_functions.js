function add_formset_row(e) {
    e.preventDefault();

    // Get the current number of items
    var count = $(".formset-row").length;

    // Get the template and replace it with the proper item ID
    var template = $("#formset-template").html();
    var replacedTemplate = template.replace(/__prefix__/g, count);

    // Add the replaced template after the last formset-row
    $("#form_content hr").last().after(replacedTemplate);

    // Update the form count
    $("[id$=TOTAL_FORMS").val(count + 1);
}

function show_help_text(e, button) {
    e.preventDefault();

    const helpText = button.dataset.helpText;
    // TODO: Change this to a modal
    alert(helpText);
}

$(document).ready(function () {
    $("#add-formset-row").on("click", function (e) {
        add_formset_row(e);
    });

    $(".input-help").on("click", function(e) {
        show_help_text(e, this);
    })
});
