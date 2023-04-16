document.getElementById("venue_name").value = sessionStorage.getItem('uvenue_name');
document.getElementById("venue_place").value = sessionStorage.getItem('uvenue_place');
document.getElementById("venue_loc").value = sessionStorage.getItem('uvenue_loc');
document.getElementById("venue_cap").value = sessionStorage.getItem('uvenue_cap');
document.getElementById("venue_id").value = sessionStorage.getItem('uvenue_id');
console.log(sessionStorage.getItem('uvenue_id'));


function venuedelete(){
    document.getElementById("venue_id").value = sessionStorage.getItem('uvenue_id');
    location.href='deletevenue'
}