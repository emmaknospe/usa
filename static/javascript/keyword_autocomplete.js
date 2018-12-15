$(function() {
    $(".key-word-autocomplete").each(function() {
        let autocomplete = this;
        // set up searching bound to input
        $(autocomplete).find("input.key-word-autocomplete-input").on("input", function() {
            let value = $(this).val();
            let input_element = this;
            if (value !== "") {
                $.get(Urls['get-similar-key-words'](value), function(data) {
                    $(autocomplete).find(".key-word-autocomplete-menu").html(data).prop("hidden", false);

                    let highlighted_index = 0;
                    let key_word_autocomplete_recommendations =
                        $(autocomplete).find(".key-word-autocomplete-recommendation");
                    let list_length = key_word_autocomplete_recommendations.length;
                    key_word_autocomplete_recommendations.click(function() {
                        value = $(this).attr("data-value");
                        $(input_element).val(value);
                        $(autocomplete).find(".key-word-autocomplete-menu").prop("hidden", true);
                    });
                    $(input_element).keydown(function(event) {
                        if (event.keyCode === 40) {
                            highlighted_index++;
                            event.preventDefault();
                        } else if (event.keyCode === 38) {
                            highlighted_index--;
                            event.preventDefault();
                        } else if (event.keyCode === 13) {
                            if (highlighted_index > 0) {
                                value = key_word_autocomplete_recommendations.eq(highlighted_index - 1).attr("data-value");
                                $(input_element).val(value);
                                $(autocomplete).find(".key-word-autocomplete-menu").prop("hidden", true);
                            }
                            event.preventDefault();
                        }
                        if (highlighted_index === list_length + 1) {
                            highlighted_index = 0;
                        }
                        key_word_autocomplete_recommendations.removeClass("active");
                        if (highlighted_index > 0) {
                            key_word_autocomplete_recommendations.eq(highlighted_index - 1).addClass("active")
                        }
                    });
                });
            } else {
                $(autocomplete).find(".key-word-autocomplete-menu").prop("hidden", true);
            }
        });
        // set up blanking on lack of focus
        $(autocomplete).focusout(function() {
            // check if focus out occurred within drop down area, in this case we don't process the focus out
            // and process the click instead.
            if ($(autocomplete).find(".key-word-autocomplete-menu:hover").length) {
                return;
            }
            $(autocomplete).find(".key-word-autocomplete-menu").prop("hidden", true);
        });
    });
});