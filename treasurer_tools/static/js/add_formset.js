// TODO: Remove when form redesign complete
function add_formset_row(e) {

    e.preventDefault();

    // Get the current number of items
    var count = $(".formset-row").length;

    // Get the template and replace it with the proper item ID
    var template = $("#item-template").html();
    var replacedTemplate = template.replace(/__prefix__/g, count);

    // Add the replaced template after the last formset-row
    $("#transaction-items").last().after(replacedTemplate);

    // Update the form count
    $("[id$=TOTAL_FORMS").val(count + 1);
}

$(document).ready(function () {
    $("#add-formset-row").on("click", function (e) {
        add_formset_row(e);
    });
});
