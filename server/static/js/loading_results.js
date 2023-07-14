async function createSocketAndConnect(exploit_task_id) {
    const waitSocket = await new WebSocket(
        'ws://' + window.location.host + '/loading_results/' + exploit_task_id
    );

    waitSocket.onmessage = function (message) {
        var text = message.data;
        const data = JSON.parse(text);
        if (data.finish === 1 && data.task_id === exploit_task_id){
            document.getElementById(
                "link_to_download").setAttribute(
                    "href",
                    "/download_results?task_id="+exploit_task_id);
        }
    }

    waitSocket.onclose = function (e) {
    }

    waitSocket.onopen = function () {
        waitSocket.send('{"task_id": '+ exploit_task_id +'}')
    }

}