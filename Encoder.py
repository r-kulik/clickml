import pickle
from sklearn.preprocessing import OneHotEncoder


class Encoding:
    def __init__(self, trial_number):
        self.encoderCategories = []
        self.encoders = []
        self.trial_number = trial_number

    def save(self):
        with open("encoder_{}.pickle".format(self.trial_number), "wb") as fout:
            pickle.dump(self, fout)

    def fit(self, x):
        for i in x:
            if x[i].dtype == object:
                x, encoder = self.fit_enc(x, i)
                self.encoderCategories.append(i)
                self.encoders.append(encoder)
        return x


    def fit_enc(self, x, category):
        encoder = OneHotEncoder()
        x_encode = encoder.fit_transform(x[[category]]).toarray()
        x[encoder.categories_[0]] = x_encode
        x = x.drop(category, axis=1)
        return x, encoder

    def transform(self, x):
        for enc, category in zip(self.encoders, self.encoderCategories):
            x_encode = enc.transform(x[[category]]).toarray()
            x[enc.categories_[0]] = x_encode
            x = x.drop(category, axis=1)
        return x

    def save_best(self):
        with open("best_encoder.pickle", "wb") as fout:
            pickle.dump(self, fout)
        return 0
