$(document).ready(function () {
    $('#example').DataTable({
        "processing": true,
        "ajax": "/admin/sim",
        "columns": [

            {"data": "sr_no"},
            {"data": "sim_no"},
            {"data": "tsp"},
            {"data": "lsa"},
            {"data": "issue_date"}
        ]
    });
});
