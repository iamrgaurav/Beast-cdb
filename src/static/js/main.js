$('#aadhaar').bind('input', function (e) {
    e.target.value = e.target.value.replace(/[^\d]/g, '').replace(/(.{4})/g, '$1 ').trim();
  });
$('button#success').click(function () {
   $("div.success").css("display", "none");
      setTimeout(function(){
       $('#myModal').modal('show');
   }, 5000);
});