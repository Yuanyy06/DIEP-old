#-*- coding = utf-8 -*-
# @Time :       2021/02/22 22:22
# @Author :     Yuanyy
# @File :       2_FeatureSelection.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score, average_precision_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')

input = "DIEP\\ML\\Trainingset\\DownSampledTrainingSet\\"
output = "DIEP\\results\\"

#
oob_mean = []
Accuracy_mean = []
Recall_mean = []
Precision_mean = []
F1score_mean = []
AUC_mean = []
PR_mean = []
RF = RandomForestClassifier(random_state=10, oob_score=True)
# initial features, 20 in total
features =['Recs.add','Recs.sub','EssgCom','GOSemSim_MF','GOSemSim_BP','GOSemSim_CC','GeneMANIAGG','HI.add','HI.sub','BioDis','LofIn.add',
            'LofIn.sub','BioGRIDPP','STRINGPP','REAC_FI','PS_2DbJacSim','HighexpPer','Abundance.add','COXPRESdbMRvalue','DOSemSim']
delf = -1
for f in range(20):
    # the first time, no feature is deleted
    print(20-f)
    if delf is not -1:
        del features[delf]
    #
    oob_score = []
    Accuracy = []
    Recall = []
    Precision = []
    F1score = []
    AUC = []
    PR = []
    for i in range(200):
        Training = pd.read_table(input + "Trainingset" + str(i + 1) + ".txt", na_values=".")
        X, y = Training[features], Training["Class"]
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
        if i == 0:
            FeatureImportance = pd.concat([pd.DataFrame(X.columns, columns=["Feature"]), pd.DataFrame(RF.feature_importances_, columns=["Importance" + str(i + 1)])],axis=1)
        else:
            FeatureImportance = pd.concat([FeatureImportance, pd.DataFrame(RF.feature_importances_, columns=["Importance" + str(i + 1)])], axis=1)
    FIvalue = FeatureImportance.drop(labels="Feature", axis=1)
    mean = pd.concat([pd.DataFrame(FeatureImportance.iloc[:, 0]), pd.DataFrame(FIvalue.mean(1), columns=["Mean_Importance"])], axis=1)
    print("Delete feature: " + mean.iloc[mean.iloc[:, 1].idxmin(), 0])
    mean.to_csv(output + "Del-" + mean.iloc[mean.iloc[:, 1].idxmin(), 0] +".txt", sep="\t", index=False)
    delf = mean.iloc[:, 1].idxmin()
    oob_mean.append(np.mean(oob_score))
    Accuracy_mean.append(np.mean(Accuracy))
    Recall_mean.append(np.mean(Recall))
    Precision_mean.append(np.mean(Precision))
    F1score_mean.append(np.mean(F1score))
    AUC_mean.append(np.mean(AUC))
    PR_mean.append(np.mean(PR))

# output
Results = open("F:\\DigenicProg\\20211109\\ML\\FeatureSelection\\FeatureSelectionparas_training.txt", "a")
Results.write("Count" + "\t" + "oob_score" + "\t" + "Accuracy" + "\t" + "Recall" + "\t" + "Precision" + "\t" + "F1score" + "\t" + "AUC" + "\t" + "PR" + "\n")
fnum = list(range(20, 0, -1))
for m in list(range(oob_mean.__len__())):
    Results.write(str(20 - m) + "\t" + str(oob_mean[m]) + "\t" + str(Accuracy_mean[m]) + "\t" + str(Recall_mean[m]) + "\t" + str(Precision_mean[m]) + "\t" + str(F1score_mean[m]) + "\t" + str(AUC_mean[m]) + "\t" + str(PR_mean[m]) + "\n")
Results.write("0\t.\t.\t.\t.\t.\t.\t" + X.columns[0])
Results.close()



