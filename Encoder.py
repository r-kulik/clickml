import pickle
from sklearn.preprocessing import OneHotEncoder
from WorkWithTask import Task


class Encoding:
    def __init__(self):
        self.encoderCategories = []
        self.encoders = []

    def save(self, trial_number, task: Task):
        with open("task_{}/encoder_{}.pickle".format(task.task_id, trial_number),
                  "wb") as fout:
            pickle.dump(self, fout)

    def fit(self, x):
        for i in x:
            if x[i].dtype == object:
                x, encoder = self.fit_enc(x, i)
                self.encoderCategories.append(i)
                self.encoders.append(encoder)
        return x

    @staticmethod
    def fit_enc(x, category):
        encoder = OneHotEncoder()
        x_encode = encoder.fit_transform(x[[category]]).toarray()
        x[encoder.categories_[0]] = x_encode
        x = x.drop(category, axis=1)
        return x.copy(), encoder

    def transform(self, x):
        for enc, category in zip(self.encoders, self.encoderCategories):
            x_encode = enc.transform(x[[category]]).toarray()
            x[enc.categories_[0]] = x_encode
            x = x.drop(category, axis=1)
        return x.copy()
