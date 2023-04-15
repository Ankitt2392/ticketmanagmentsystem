function displayRadioValue() {
    var ele = document.getElementsByName('stars');
      
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked){
            console.log(ele[i].value);
            document.getElementById("show").value = sessionStorage.getItem('rating_show');
            document.getElementById("venue").value = sessionStorage.getItem('rating_venue');
            document.getElementById("rating").value = ele[i].value;
            document.getElementById("rating_form").submit();
        }
    }
}