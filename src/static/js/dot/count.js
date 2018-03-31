$(document).ready(function () {
    $('#myTable').DataTable({
        "scrollx": true,
        "ajax": '/admin/by-count',
        "columns": [

            {"data": "aadhaar"},
            {"data": "count"}
        ]
    });
});
