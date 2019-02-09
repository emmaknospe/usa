let type_to_add = "";
let create = true;
let question_id = -1;
$(function() {
    let questions_added = 0;
    $("#question-type-selector").change(function() {
        $(".question-description").hide();
        if ($(this).val() !== "NONE") {
            $("#question-add-btn").prop("disabled", false);
            $("#" + $(this).val() + "-description").show();
        } else {
            $("#question-add-btn").prop("disabled", true);
        }
    });

    $("#question-add-btn").click(function() {
        if (!$(this).prop("disabled")) {
            let to_add = $("#question-type-selector").val();
            $.get(Urls['create-question'](to_add), function(data) {
                $("#create-question-modal-body").html(data);
                $("#question-modal-title").text("Create New Question");
                $("#create-modal").addClass("active");
                type_to_add = to_add;
                create = true;
            });
        }
    });
    $("#create-question-save").click(function(){
        $("#create-modal").removeClass("active");
        let question_data = $("#question-creation-form").serializeArray().reduce(function(obj, item) {
                    obj[item.name] = item.value;
                    return obj;
                }, {});
        $.post(
            Urls['edit-question-save'](),
            {
                form_data: JSON.stringify(question_data),
                create: create,
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                application_id: window.APPLICATION_ID,
                type: type_to_add,
                question_id: question_id
            },
            function (data) {
                if (create) {
                    let questions_area = $("#questions-area");
                    if (questions_added === 0) {
                        questions_area.html("");
                    }
                    questions_area.append(data);
                    questions_added++;
                } else {
                    let old_question = $("#question-wrapper-" + question_id);
                    old_question.replaceWith(data);
                }
                rebind();
            }
        );
    });

    $("#create-question-cancel").click(function() {
        $("#create-modal").removeClass("active");
    });
    bind();
});

function rebind() {
    $(".delete-question").off("click");
    $(".edit-question").off("click");
    bind();
}
function bind() {
    $(".delete-question").click(function() {
        let qid = $(this).data("question-id");
        $.post(
            Urls['delete-question']($(this).data("question-id")),
            {csrfmiddlewaretoken: window.CSRF_TOKEN},
            function(data) {
                if (data['status'] === 'success') {
                    $("#question-wrapper-" + qid).remove();
                    questions_added--;
                }
            },
            "json"
        );
    });
    $(".edit-question").click(function() {
        question_id = $(this).data("question-id");
        $.get(Urls['edit-question'](question_id), function(data) {
            $("#create-question-modal-body").html(data);
            $("#question-modal-title").text("Create New Question");
            $("#create-modal").addClass("active");
            create = false;

        });
    });
}