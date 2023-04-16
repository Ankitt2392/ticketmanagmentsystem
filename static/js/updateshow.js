document.getElementById("show_name").value = sessionStorage.getItem('ushow_name');
document.getElementById("show_rat").value = sessionStorage.getItem('ushow_rating');
document.getElementById("show_tag").value = sessionStorage.getItem('ushow_tag');
document.getElementById("price").value = sessionStorage.getItem('ushow_price');
document.getElementById("show_time_start").value = sessionStorage.getItem('ushow_time');
document.getElementById("show_id").value = sessionStorage.getItem('ushow_showid');

console.log(sessionStorage.getItem('ushow_showid'));


function showdelete(){
    document.getElementById("show_id").value = sessionStorage.getItem('ushow_showid');
    location.href='deleteshow'
}