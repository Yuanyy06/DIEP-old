#-*- coding = utf-8 -*-
# @Time :       2021/02/23 12:00
# @Author :     Yuanyy
# @File :       4_DownSampleRF.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import pickle
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from treeinterpreter import treeinterpreter as ti
from sklearn.metrics import accuracy_score, average_precision_score, recall_score, precision_score
import warnings
warnings.filterwarnings('ignore')
from Utils import *

# input files
input = ""
output = ""
# positive
DIDA = pd.read_table("DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From", "Abundance.sub", "PS_2DbJacSim", "BioGRIDPP", "EssgCom"]]

# input adjusted paras
best_para = pd.read_table("adjust_best_params.txt", na_values=".")

oob_score = []
Accuracy = []
Recall = []
Precision = []
F1score = []
AUC = []
PR = []
cv10 = []
for i in list(range(200)):
    print("Model " + str(i + 1))
    Training = pd.read_table("Trainingset" + str(i + 1) + ".txt", na_values=".")
    X, y = Training[features], Training["Class"]

    RF = RandomForestClassifier(n_estimators=best_para.iloc[i,1], max_depth=best_para.iloc[i,2], min_samples_split=best_para.iloc[i,3], min_samples_leaf=best_para.iloc[i,4], max_features=best_para.iloc[i,5], random_state=10, oob_score=True, n_jobs=10)

    RF.fit(X, y)
    y_predprob = (RF.predict_proba(X))[:, 1]
    y_pred = RF.predict(X)
    R = recall_score(y, y_pred)
    P = precision_score(y, y_pred)
    F1 = 2 * P * R / (P + R)
    oob_score.append(RF.oob_score_)
    Accuracy.append(accuracy_score(y, y_pred))
    Recall.append(R)
    Precision.append(P)
    F1score.append(F1)
    AUC.append(metrics.roc_auc_score(y, y_predprob))
    PR.append(average_precision_score(y, y_predprob))
    # cross validation
    CV10 = cross_val_score(RF, X, y, cv=10, scoring="f1", n_jobs=10)
    cv10.append(CV10.mean())

    if i == 0:
        Tra_prob = pd.DataFrame(y_predprob, columns=["prob" + str(i + 1)])
        FeatureImportance = pd.concat([pd.DataFrame(X.columns, columns=["Feature"]), pd.DataFrame(RF.feature_importances_, columns=["Importance" + str(i + 1)])], axis=1)
    else:
        Tra_prob = pd.concat([Tra_prob, pd.DataFrame(y_predprob, columns=["prob" + str(i + 1)])], axis=1)
        FeatureImportance = pd.concat([FeatureImportance, pd.DataFrame(RF.feature_importances_, columns=["Importance" + str(i + 1)])], axis=1)

    # use treeinterpreter to calculate contribution
    instances_X = X.values
    prediction_X, bias_X, contributions_X = ti.predict(RF, instances_X)
    for q in range(len(contributions_X)):
        if q == 0:
            tmp = pd.concat([pd.DataFrame(features, columns=["Feature"]), pd.DataFrame(contributions_X[q], columns=["model" + str(i + 1) + "_" + str(q + 1) + "_" + str(0), "model" + str(i + 1) + "_" + str(q + 1) + "_" + str(1)])], axis=1)
        else:
            tmp = pd.concat([tmp, pd.DataFrame(contributions_X[q], columns=["model" + str(i + 1) + "_" + str(q + 1) + "_" + str(0), "model" + str(i + 1) + "_" + str(q + 1) + "_" + str(1)])], axis=1)
    tmp.to_csv(output + "TI/ti_Tra_Contributions_" + str(i + 1) + ".txt", sep="\t", index=False)

    # output
    model_name = output + "Model\\RF_finalized_model_" + str(i + 1) + ".mdl"
    pickle.dump(RF, open(model_name, "wb"))

# output
Tra_prob.to_csv(output + "ModelPara\\ProbforTraningSet.txt", sep="\t", index=False)
FeatureImportance.to_csv(output+"ModelPara\\FeatureImportance.txt", sep="\t", index=False)

# output
Results = open(output + "ModelPara\\Test_Results.txt", "a")
Results.write("Count" + "\t" + "oob_score" + "\t" + "Accuracy" + "\t" + "Recall" + "\t"  + "Precision" + "\t" + "F1score" + "\t" + "AUC" + "\t" + "PR" + "\t" + "cv10_f1" + "\n")
for m in list(range(200)):
    Results.write(str(m+1) + "\t" + str(oob_score[m]) + "\t" + str(Accuracy[m]) + "\t" + str(Recall[m]) + "\t" + str(Precision[m]) + "\t" + str(F1score[m]) + "\t" + str(AUC[m]) + "\t" + str(PR[m]) + "\t" + str(cv10[m]) + "\n")
Results.close()

