import os


def choose_best(task, number_of_best_trial):
    for i in ["config_best.json", "encoder_best.pickle", "scaler_best.pickle", "model_best.pickle"]:
        if "{}".format(i) in os.listdir("task_{}".format(task.task_id)):
            return None

    os.rename("task_{}/config_{}.json".format(task.task_id, number_of_best_trial),
              "task_{}/config_best.json".format(task.task_id))
    os.rename(
        "task_{}/encoder_{}.pickle".format(task.task_id, number_of_best_trial),
        "task_{}/encoder_best.pickle".format(task.task_id))
    os.rename("task_{}/scaler_{}.pickle".format(task.task_id, number_of_best_trial),
              "task_{}/scaler_best.pickle".format(task.task_id))
    os.rename("task_{}/model_{}.pickle".format(task.task_id, number_of_best_trial),
              "task_{}/model_best.pickle".format(task.task_id))

    dirs = os.listdir("task_{}".format(task.task_id))
    try:
        for i in dirs:
            if "best" not in i:
                os.remove("task_{}/{}".format(task.task_id, i))
    except Exception as e:
        print(e)

