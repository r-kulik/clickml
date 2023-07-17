

class LearningModelInfo{
    constructor(
        model_id, metric_value_element_id, learning_model_id_value_element_id, progress_value_element_id
    ) {
        this.model_id = model_id;
        this.metric_value_element_id = metric_value_element_id;
        this.learning_model_id_value_element_id = learning_model_id_value_element_id;
        this.progress_value_element_id = progress_value_element_id;
    }



}

let learning_models = []



function redirectToModelCreation(){
    location.href = '/create_new_model';
}


function updateProgressBars(learning_model, data) {

    // эта функция вызывается, когда призодит сообщение с новым статусом обучения и значением целевой метрики

    // прогресс выполнения лежит в переменной data.completion_percentage
    // она принимаает значения от 0 до 1
    // значение основной метрики качества модели лежит в переменной data.main_metric_value
    // она тоже принимает значения от 0 до 1



    CP = Math.ceil(data.completion_percentage * 100);
    document.getElementById(
        learning_model.progress_value_element_id
    ).setAttribute('style', 'width: ' + CP + '%')
    document.getElementById(
        learning_model.metric_value_element_id
    ).innerText = data.main_metric_value;
    document.getElementById("waiting_gpu_response_text").setAttribute(
        'style', "display: none;"
    );
}

function visualizeException(learning_model, data){
    // эта функция вызывается когда приходит сообщение об ошибке обучения

    //  в переменной data.exception лежит текст ошибки, которую нужно показать

    let errorTextElement = document.getElementById("error_text");
    errorTextElement.innerText = data.exception;
    errorTextElement.setAttribute(
        "style", "display: grid;"
    );
}


function completeTask(learning_model, data){
    // эта функция вызывается, когда задача обучения выполнена

    // в learning_model.model_is лежит айдишник выполненной задачи
    document.getElementById(
        "a_" + learning_model.model_id
    ).setAttribute('href', '/use_model?model_id='+ data.ml_model_id);
}


/*
Ниже этой линии ничего не трогать
==================================================================================
 */

function delete_model(model_id){
    let model_object = document.getElementById(
        "ml_model_" + model_id
    );
    let xml_http_request = new XMLHttpRequest();
    xml_http_request.onreadystatechange = function() {
        if (xml_http_request.readyState === 4 && xml_http_request.status === 200){
            if (xml_http_request.responseText === "OK"){
                model_object.setAttribute(
                    "style", "display: none;"
                );
            }
        }
    }
    let request_parameters = "model_id="+model_id;
    xml_http_request.open(
        "GET",
        '/delete_model' + "?" + request_parameters,
        true);
    xml_http_request.send(null);
}


async function createSocketAndConnect(){
    const updateSocket = await new WebSocket(
        "ws://" + window.location.host + '/learning_results/'
    );



    updateSocket.onopen= function () {
        let list_to_send = [];
        for (let i = 0; i < learning_models.length; i++){
            list_to_send.push(learning_models[i].model_id);
        }
        // alert(list_to_send);
        const objectToSend = {"learning_task_id_list": list_to_send};
        updateSocket.send(
            JSON.stringify(objectToSend)
        )
        // alert(JSON.stringify(objectToSend));
    }

    updateSocket.onmessage = function (message) {
        const data = JSON.parse(message.data);
        for (let i = 0; i < learning_models.length; i++){
            let learning_model = learning_models[i];
            if (learning_model.model_id === data.learning_task_id){
                console.log(data);
                if (data.exception_occurred === 1){
                    visualizeException(learning_model, data);
                }
                if (data.complete === 1){
                    completeTask(learning_model, data);
                    return;
                }
                updateProgressBars(learning_model, data);
            }
        }

    }
}




