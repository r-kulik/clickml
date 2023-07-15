import requests
from APICONFIG import site_host


def send_percent(counter: int, n: int, task_id: int, score: float) -> bool:
    result = counter / n

    response = requests.get(
        url=f'http://{site_host}/accept_percent',
        params={
            "learning_task_id": str(task_id),
            "completion_percentage": str(result),
            "main_metric_value": str(score)
        }
    )
    return response.status_code == 200
