function add_item_row(e) {

    e.preventDefault();

    // Get the current number of items
    var count = $(".account-row").length;

    // Get the template and replace it with the proper item ID
    var template = $("#account-form-template").html();
    var replacedTemplate = template.replace(/__prefix__/g, count);

    // Add the replaced template after the last item-row
    $("#form_content hr").last().after(replacedTemplate);

    // Update the form count
    $("#id_account_set-TOTAL_FORMS").val(count + 1);
}

$(document).ready(function () {
    $("#add-account-row").on("click", function (e) {
        add_item_row(e);
    });
});