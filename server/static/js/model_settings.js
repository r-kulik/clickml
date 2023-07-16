let is_checked_one = false;
let old_label;

function showValue(id) {
    const radios = document.getElementsByName('target_variable');
    for (let i = 0; i < radios.length; i++) {

        if (radios[i].checked) {
            document.getElementById('text').innerHTML = radios[i].value;
            const label = document.getElementById(id + "1");
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