from sklearn.linear_model import LogisticRegression

def train_classifier(features, labels):
    clf = LogisticRegression(max_iter=1000)
    clf.fit(features, labels)
    return clf

def predict_label(clf, features):
    return clf.predict(features)
