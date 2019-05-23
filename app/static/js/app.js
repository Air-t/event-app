/* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  document.body.style.backgroundColor = "rgba(0,0,0,0.2)";
}

$(document).ready(function() {

    // side nav open/close toggle funtionality
    var clickState = 0;
    var btn = document.querySelector('.navbar-toggler-icon');

    btn.addEventListener('click', function(e){
      console.log(clickState);
      if (clickState == 0) {
        console.log('here');
        openNav();
        clickState = 1;
      } else {
        console.log('there');
        closeNav();
        clickState = 0;
      }
    });

    // datepicker functionality
    $("#datetimepicker1").datetimepicker({
      format: 'DD/MM/YYYY HH:mm',
    });
    $("#datetimepicker2").datetimepicker({
      format: 'DD/MM/YYYY HH:mm',
    });

    // confirm delete on click while deleting objects
    $('div.card').on('click', '.delete', function(e){
      var x = confirm("Are you sure you want to delete?");
      return (x) ? true : e.preventDefault()
    })

});
