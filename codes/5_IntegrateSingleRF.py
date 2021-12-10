#-*- coding = utf-8 -*-
# @Time :       2021/02/23 13:33
# @Author :     Yuanyy
# @File :       5_IntegrateSingleRF.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import pandas as pd
import numpy as np
import pickle
from Utils import *
from sklearn.metrics import accuracy_score, average_precision_score, recall_score, precision_score
from sklearn import metrics

input = ""
modelinput = ""
TestDatainput = ""
output = ""

# positive
DIDA = pd.read_table(input + "Original\\DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From", "Abundance.sub", "PS_2DbJacSim", "BioGRIDPP", "EssgCom"]]
cvfile = pd.read_table(modelinput + "ModelPara\\Test_Results.txt")
# negative
DIDA_NDI = pd.read_table(input + "Delt\\Training_DIDA_NDI_FV.txt", na_values=".")
Random = pd.read_table(input + "Delt\\Training_Random_FV.txt", na_values=".")

# test
DIDA_NDIt = pd.read_table(input + "Delt\\Test_DIDA_NDI_FV.txt", na_values=".")
Randomt = pd.read_table(input + "Delt\\Test_Random_FV.txt", na_values=".")
Alltest = pd.concat([DIDA_NDIt, Randomt], axis=0, ignore_index=True)

# load the model from disk
ModelNum = [2, 6, 10, 12, 15, 36, 55, 58, 65, 69, 77, 79, 87, 106, 109, 117, 120, 127, 145, 149, 160, 178, 179, 181, 182, 199]  # 17个特征，调参
ModelIndex = [x-1 for x in ModelNum]
ModelList = []
for i in ModelIndex:
    modelname = modelinput + "Model\\RF_finalized_model_" + str(i + 1) + ".mdl"
    model = pickle.load(open(modelname, 'rb'))
    ModelList.append(model)

# weighting according to 10x-cv-f1
Test_obb = list(cvfile.iloc[ModelIndex, 8])
weight = [(Test_obb[i] / sum(Test_obb)) for i in range(len(Test_obb))]

# Predict
Alltraining = pd.concat([DIDA, DIDA_NDI, Random], axis=0, ignore_index=True)
X, y = Alltraining[features], Alltraining["Class"]

Allprob = []
for count in list(range(len(ModelList))):
    # print(count)
    predprob = ModelList[count].predict_proba(X)[:, 1]
    predprob_c = [predprob[i] * weight[count] for i in range(len(X))]
    Allprob.append(pd.DataFrame(predprob_c))
    if count == 0:
        prob_add = predprob_c
    else:
        prob_add = [predprob_c[i] + prob_add[i] for i in range(len(prob_add))]
final_prob = pd.concat([pd.DataFrame(Alltraining.iloc[:, 0:4]), pd.DataFrame(prob_add, columns=["Predprob"])], axis = 1)
final_prob.to_csv(output + "AllTraining_final_predprob.txt", sep="\t", index=False)

# test set
Testset = ""
Xt, yt = Testset[features], Testset["Class"]
for count in list(range(len(ModelList))):
    predprob = ModelList[count].predict_proba(Xt)[:, 1]
    predprob_c = [predprob[i] * weight[count] for i in range(len(Xt))]
    if count == 0:
        prob_add = predprob_c
    else:
        prob_add = [predprob_c[i] + prob_add[i] for i in range(len(prob_add))]
final_prob = pd.concat([pd.DataFrame(Testset.iloc[:, 0:4]), pd.DataFrame(prob_add, columns=["Predprob"])], axis = 1)
final_prob.to_csv(output + "AllTest_final_predprob.txt", sep="\t", index=False)
