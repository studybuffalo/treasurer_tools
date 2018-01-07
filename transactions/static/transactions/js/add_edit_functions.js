function update_financial_code(yearSelect) {
    const $yearSelect = $(yearSelect);
    const $fieldset = $yearSelect.closest("fieldset");
    const $codeSelect = $fieldset.find('[id*="-code"]');
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

                if ($option.attr("data-year_id") == yearID) {
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

$(document).ready(function () {
    $('[id*="-budget_year"]').on("change", function () {
        reset_financial_code(this)
        update_financial_code(this);
    });

    // Run an initial update on all selects
    $('[id*="-budget_year"]').each(function (index, select) {
        console.log(select)
        update_financial_code(select);
    });
});