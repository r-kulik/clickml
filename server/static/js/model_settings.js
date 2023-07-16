// Вношу изменения sfksndkjfnkj

var is_checked_one = false;
var old_label;
function showValue(id) {
    var radios = document.getElementsByName('target_variable');
    for (var i = 0; i < radios.length; i++) {

        if (radios[i].checked) {
            document.getElementById('text').innerHTML = radios[i].value;
            var label = document.getElementById(id+"1");
            label.style.background = "#79E34F";
            if(is_checked_one){
                old_label.style.background = 'initial';
                is_checked_one = false;
            }
            old_label = label;
            is_checked_one = true;

            break;

        }
    }


}