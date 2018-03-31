$(document).ready(function () {
    $('#myTable').DataTable({
        "scrollx": true,
        "ajax": "/admin/by-lsa",
        "columns": [

            {"data": "sr_no"},
            {"data": "aadhaar"},
            {"data": "count"}
        ]
    });
});
