

$(document).ready(function() {
    $(".todo-checkbox").change(function() {
        var todoId = $(this).val();
        var titleElement = $("#title-" + todoId);
        var editButton = $(".edit-button[data-todo-id='" + todoId + "']");
        var completed = $(this).is(":checked").toString();

        if ($(this).is(":checked")) {
            titleElement.addClass("completed");
            editButton.prop("disabled", true);
            
            
        } else {
            
            editButton.addClass("editButton")
            editButton.prop("disabled", false);
        }

        // Send an AJAX request to update the server-side status of the TODO item
        $.ajax({
            url: "/update_todo_status/" + todoId,
            type: "POST",
            data: {
                completed:  completed
            },
            success: function(response) {
                console.log("TODO status updated successfully.");
                location.reload();
            },
            error: function(error) {
                console.error("Error updating TODO status:", error);
            }
        });
    });
});
