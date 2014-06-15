function row_data(id, status) {
      return '<tr id="task'+id+'"><td>'+id+'</td><td>'+status+'</td></tr>';
}

function update_table() {
    $.ajax({
        type: "GET",
        url: "/api/v1/tasks/",
        dataType: "json",
        success: function(response) {
            var tasks = $("#tasks").find("tbody");
            var task_data = response.tasks;

            // Keep the job id up to date
            $("#jobid").html(response.job);

            // For all tasks in the response, update or create a row
            var count = 0;
            $.each(task_data, function(id, status) {
                var row = tasks.find("#task" + id);
                if (row.length) {
                    row.replaceWith(row_data(id, status));
                } else {
                    tasks.append(row_data(id, status));
                }
                count++;
            });

            // If we iterated over fewer tasks in the response
            // then reduce the number of table rows to match.
            count--;
            tasks.find("tr:gt(" + count + ")").remove();

        },
        error: function(response) {
            alert("FAILED");
        }
    })
}