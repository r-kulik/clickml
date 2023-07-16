import threading
import time

import requests
from APICONFIG import site_host
import logging
from Clear import clear_files_after_error




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


def send_error_message(e: Exception, task_id: int, purpose: str):


    logging.basicConfig(filename="py_log.log", filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)

    logging.info(str(e))

    if purpose == "learn":
        url_destination = "report_learning_task_exception"
    else:
        url_destination = "report_exploit_task_exception"
    web_thread = threading.Thread(
        target=send_error_message_to_host,
        args=[
            url_destination,
            task_id,
            e
        ]
    )
    web_thread.start()

    clear_files_after_error(task_id)




def send_error_message_to_host(
        url_destination: str,
        task_id: int,
        e: Exception
) -> None:
    time.sleep(2)
    requests.post(
        url=f"http://{site_host}/{url_destination}",
        json={
            "taskId": task_id,
            "exceptionText": str(e)
        }
    )
