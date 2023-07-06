from WorkWithTask import Task
from DataSending import send_fail_message
from Predict import Predict
import logging
from OptunaPreprocessing import OptunaWork

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    # while True:
    task = Task()

    if task.is_correct:
        if task.purpose == "learning":
            OptunaWork(task).optuna_study()
        elif task.purpose == "using":
            a = Predict(task).predict()
            print(a)
            # todo normal output
        else:
            logging.debug("Wrong task_type format")
    else:
        send_fail_message()
