import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def read_csv(filepath):
    df = pd.read_csv(filepath)

    return df.columns


def train_model(train_input, train_classes, eval_input, train_filepath, eval_filepath):
    # training input
    train_df = pd.read_csv(train_filepath)
    X_train = train_df[train_input]

    # evaluation input
    test_df = pd.read_csv(eval_filepath)
    X_test = test_df[eval_input]

    # training classes
    # convert group variable to list
    train_groups = train_df[train_classes].tolist()

    # build group dictionary
    groups = train_df[train_classes].tolist()
    uq_groups = set(groups)

    group_dict = {}
    i=0
    for x in uq_groups:
      group_dict[x] = i
      i = i+1

    # map classes to categories, and vice versa
    Y_train = []
    for x in train_groups:
      num = group_dict.get(x)
      Y_train.append(num)

    # run model, predict categories for eval dataset
    test_predicted = run_model(X_train, Y_train, X_test)

    # map categories to classes
    inv_group_dict = {}
    j = 0
    for x in uq_groups:
      inv_group_dict[j] = x
      j = j+1

    # convert categorical prediction to text
    test_groups = []
    for x in test_predicted:
      groupname = inv_group_dict.get(x)
      test_groups.append(groupname)


    test_df.insert(loc=len(test_df.columns),column='predicted_classification', value=test_groups)

    test_df.to_csv("data/output.csv", index=False)

    return 1



def run_model(X_train, Y_train, X_test):
    # bag of words
    count_vect = CountVectorizer()

    # use bag of words to transform each phrase into a vector
    X_train_counts = count_vect.fit_transform(X_train)

    # give less weight to common words
    # equalize short and long descriptions
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


    # classify using naive bayes
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, Y_train)


    X_test = X_test.replace(np.nan, '', regex=True)


    test_counts = count_vect.transform(X_test)

    # use the classifier to predict
    test_predicted = clf.predict(test_counts)

    return test_predicted