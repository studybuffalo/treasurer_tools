function update_group_and_year() {
    const systemID = $("#id_code_system").val();
    const $groupSelect = $("#id_code_group");
    const $groupOptions = $groupSelect.children();
    const $yearSelect = $("#id_budget_year");
    const $yearOptions = $yearSelect.children();

    // Reset the group and budget year selections
    $groupSelect.val("");
    $yearSelect.val("");

    if (systemID) {
        // Show code group options with data_system_id matching systemID
        $groupOptions.each(function (index, option) {
            let $option = $(option);

            if ($option.attr("data-system_id") == systemID) {
                $option.prop("hidden", false);
            } else {
                $option.prop("hidden", true);
            }
        });

        // Show budget year options with data_system_id matching systemID
        $yearOptions.each(function (index, option) {
            let $option = $(option);

            if ($option.attr("data-system_id") == systemID) {
                $option.prop("hidden", false);
            } else {
                $option.prop("hidden", true);
            }
        });

        // Enable the selects
        $groupSelect.prop("disabled", false)
        $yearSelect.prop("disabled", false)
    } else {
        // No system selected - disable group and year selects
        $groupSelect.prop("disabled", true)
        $yearSelect.prop("disabled", true)
    }
}

function initial_update_group_and_year() {
    // No system selected - disable group and year selects
    if (!$("#id_code_system").val()) {
        $("#id_code_group").prop("disabled", true)
        $("#id_budget_year").prop("disabled", true)
    }
}

$(document).ready(function () {
    $("#id_code_system").on("change", function () {
        update_group_and_year();
    });

    initial_update_group_and_year();
});
