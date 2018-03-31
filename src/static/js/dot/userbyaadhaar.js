$(document).ready(function () {
    console.log($.get('/user/sim'));
    $('#myTable').DataTable({
        "scrollx": true,
        "ajax": "/user/sim",
        "columns": [

            {"data": ""},
            {"data": ""},
            {"data": ""},
            {"data": ""},
            {"data": ""}
        ]
    });
});
