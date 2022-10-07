$(document).ready(function () {
    const input_field = $("#full_search_input");
    const button = $("#full_text_search_btn");

    input_field.on("input", function () {
        button.prop('disabled', input_field.val().length === 0);
    })

    button.click(function (event) {
        $.ajax({
            type: "GET",
            url: "full_search/" + input_field.val(),
            dataType: "json",
            encode: true,
        }).done(function (data) {
            $("#full_search_result_div").css("visibility", "visible");
            let result_list = $("#full_search_result");
            result_list.empty();
            let highlight_result_list = $("#full_search_highlight_result");
            highlight_result_list.empty();
            const title = "There is " + data['meta']['count'] + " matches for the '" + data['meta']['query'] + "' query";
            $("#full_search_count").text(title);
            $.each(data['results'], function (i, item) {
                result_list.append(
                    '<li class="list-group-item">' + item['name'] + '</li>'
                );
            });
            $.each(data['ranked_results'], function (i, item) {
                highlight_result_list.append(
                    '<li class="list-group-item">' + item['highlight'] + '</li>'
                );
            });
        });
    });
});