from WorkWithTask import Task
from DataSending import send
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    while True:
        task = Task()
        if task.task_type == "learning":
            pass

        elif task.task_type == "using":
            pass

        else:
            logging.debug("Wrong task_type format")

        send()
