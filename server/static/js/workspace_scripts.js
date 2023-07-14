

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


function updateProgressBars(learning_model, data){
    CP = Math.ceil(data.completion_percentage * 100);
    document.getElementById(
        learning_model.progress_value_element_id
    ).setAttribute('style', 'width: '+ CP +'%')
    document.getElementById(
        learning_model.metric_value_element_id
    ).innerText = data.main_metric_value;
}

function completeTask(learning_model, data){
    document.getElementById(
        "a_" + learning_model.model_id
    ).setAttribute('href', '/use_model?model_id='+ data.ml_model_id);
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
                if (data.complete === 1){
                    completeTask(learning_model, data);
                    return;
                }
                updateProgressBars(learning_model, data);
            }
        }

    }
}




