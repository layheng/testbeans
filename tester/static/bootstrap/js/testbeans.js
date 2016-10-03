// script for testbeans project
function start()
{
    var current = new Date();
    var year = current.getFullYear();
    document.getElementById("copy_right").innerHTML = "<p>&copy TEST BEANS " + year.toString() + "</p>";
 }

 window.addEventListener("load", start, false);
