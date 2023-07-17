// Функция должна вызываться в случае ошибки и рисовать нам окошко

function handleException(data){
    let errorObject = document.getElementById(
                "error_message"
            );
            errorObject.setAttribute(
                "style", "display: grid;"
            );
            errorObject.innerText = data.exception;
}

// Функция вызывается в случае корректного выполнения задания
// ссылка на скачивание файла будет /download_results?task_id="+data.task_id
function completeTask(data, exploit_task_id){
                var image = document.getElementById("loading");

            image.setAttribute("style", "display: none;")
            document.getElementById(
                "link_to_download").setAttribute(
                    "href",
                    "/download_results?task_id="+data.task_id);
            document.getElementById(
                "link_to_download").setAttribute(
                    "style",
                    "display: block;text-decoration: none;");
}


// ==================================================================================
// УВАЖАЕМЫЙ ЭРНЕСТ ГЕНРИХОВИЧ МАЦКЕВИЧ!!
// Все, что нахожится ниже этой линии, не должно представляться областью вашего интереса
// Пожалуйста, пишите свой код выше этой линии
// =================================================================================

async function createSocketAndConnect(exploit_task_id) {
    const waitSocket = await new WebSocket(
        'ws://' + window.location.host + '/loading_results/' + exploit_task_id
    );

    waitSocket.onmessage = function (message) {
        var text = message.data;

        const data = JSON.parse(text);

        if (data.exception_occurred === 1){
            handleException(data);
        }
        if (data.finish === 1 && data.task_id === exploit_task_id){
            completeTask(data, exploit_task_id);
        }
    }

    waitSocket.onclose = function (e) {
    }

    waitSocket.onopen = function () {
        waitSocket.send('{"task_id": '+ exploit_task_id +'}')
    }

}