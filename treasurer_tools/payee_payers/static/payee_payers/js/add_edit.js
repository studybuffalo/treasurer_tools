function set_country_to_canada() {
    $("#id_country option:contains('Canada')").attr("selected", "selected");
    update_province_input();
}

function update_province_input() {
    function create_options(values) {
        // Converts an array of values into an array of option elements
        var options = [];

        $.each(values, function (index, value) {
            var $option = $("<option></option>");
            $option.val(value).text(value);
            options.push($option);
        });

        return options;
    }

    // Array of Canadian provinces
    var provinces = [
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Northwest Territories",
        "Nova Scotia",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon"
    ];

    // Array of USA States
    var states = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming"
    ];

    // Get currenty country value
    var country = $("#id_country option:selected").text();

    var $newInput;

    // Create basic element
    if (country === "Canada") {
        $newInput = $("<select></select>");
        $newInput.append(create_options(provinces));
    } else if (country === "United States") {
        $newInput = $("<select></select>");
        $newInput.append(create_options(states));
    } else {
        $newInput = $("<input>");
        $newInput.attr("type", "text");
    }

    // Add required properties
    $newInput
        .attr("name", "province")
        .attr("maxlength", "100")
        .prop("required", true)
        .attr("id", "id_province");

    // Remove the old input
    var $oldInput = $("#id_province");
    var $span = $oldInput.parent();

    $oldInput.remove();

    // Add the new input
    $span.append($newInput);
}

$(document).ready(function () {
    set_country_to_canada();

    $("#id_country").on("change", function () {
        update_province_input();
    });
});