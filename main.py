from WorkWithTask import Task
from DataSending import send_fail_message
from Predict import Predict
import logging
from OptunaPreprocessing import OptunaWork
from sklearn.model_selection import train_test_split


from sklearn import metrics

def print_clf_metrics( y_actual, y_pred ):
    print(f'Testing accuracy = {metrics.accuracy_score(y_actual, y_pred)}')
    print(f'Testing precision = {metrics.precision_score(y_actual, y_pred)}')
    print(f'Testing recall = {metrics.recall_score(y_actual, y_pred)}')
    print(f'Testing F1-score = {metrics.f1_score(y_actual, y_pred)}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    # while True:
    task = Task()

    if task.is_correct:
        if task.purpose == "learning":
            OptunaWork(task).optuna_study()
        elif task.purpose == "using":
            y_test = task.df[task.target_variable]
            task.df = task.df.drop(task.target_variable, axis=1)
            a = Predict(task).predict()
            print_clf_metrics(y_test, a)
            # todo normal output
        else:
            logging.debug("Wrong task_type format")
    else:
        send_fail_message()
