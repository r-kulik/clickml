from WorkWithTask import Task
from DataSending import send_fail_message
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    while True:
        task = Task()

        if task.is_correct:
            if task.task_type == "learning":
                pass

            elif task.task_type == "using":
                pass

            else:
                logging.debug("Wrong task_type format")
        else:
            send_fail_message()
