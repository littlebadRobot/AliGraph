# Evaluation Metric for node classification and link prediction

import numpy as np
import random, math, warnings
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import *
from sklearn.metrics.pairwise import cosine_similarity

def read_label(inputFileName):
	f = open(inputFileName, "r")
	lines = f.readlines()
	f.close()
	N = len(lines)
	y = np.zeros(N, dtype = int)
	for line in lines:
		l = line.strip("\n\r").split(" ")
		y[int(l[0])] = int(l[1])

	return y

def multiclass_node_classification_eval(X, y, ratio = 0.2):
	warnings.filterwarnings("ignore")

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = ratio, random_state = 2018)
	clf = LinearSVC()
	clf.fit(X_train, y_train)

	y_pred = clf.predict(X_test)

	macro_f1 = f1_score(y_test, y_pred, average = "macro")
	micro_f1 = f1_score(y_test, y_pred, average = "micro")

	print "Classification macro_f1 = %f, micro_f1 = %f" %(macro_f1, micro_f1)

	return macro_f1, micro_f1

def link_prediction_ROC(inputFileName, Embeddings):
	f = open(inputFileName, "r")
	lines = f.readlines()
	f.close()

	X_test = []

	for line in lines:
		l = line.strip("\n\r").split(" ")
		X_test.append([int(l[0]), int(l[1]), int(l[2])])

	y_true = [X_test[i][2] for i in range(len(X_test))]
	y_predict = [cosine_similarity(Embeddings[X_test[i][0], :].reshape(1, -1), Embeddings[X_test[i][1], :].reshape(1, -1))[0,0] for i in range(len(X_test))]
	roc = roc_auc_score(y_true, y_predict)

	if roc < 0.5:
		roc = 1 - roc

	print "Evaluation ROC: " + str(roc)
	return roc

def node_classification_F1(Embeddings, y):
	print "30% train..."
	macro_f1_avg = 0
	micro_f1_avg = 0
	for i in range(10):
		macro_f1, micro_f1 = multiclass_node_classification_eval(Embeddings, y, 0.7)
		macro_f1_avg += macro_f1
		micro_f1_avg += micro_f1
	macro_f1_avg /= 10
	micro_f1_avg /= 10
	print "macro_f1 average value: " + str(macro_f1_avg)
	print "micro_f1 average value: " + str(micro_f1_avg)