const forbidden_project_names = [];


function addToForbiddenNames(name){
    forbidden_project_names.push(name);
}

function nameIsForbidden(name){
    return forbidden_project_names.includes(name);
}


window.addEventListener("load", (event) => {
    const form = document.getElementById("create_new_model_form");
    const project_name_field = document.getElementById('project_name_input');
    if (form) {
        form.addEventListener("submit", (event) => {
            if (nameIsForbidden(project_name_field.value)){
                alert("\"" + project_name_field.value +"\" is a forbidden name");
                event.preventDefault();
            }
        })
    }
});