async function createSocketAndConnect(exploit_task_id) {
    const waitSocket = await new WebSocket(
        'ws://' + window.location.host + '/loading_results/' + exploit_task_id
    );

    waitSocket.onmessage = function (message) {
        alert(message);
    }

    waitSocket.onclose = function (e) {
    }


    waitSocket.onopen = function () {
        waitSocket.send("Waiting for results from server")
    }

}