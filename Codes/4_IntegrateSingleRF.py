#-*- coding = utf-8 -*-
# @Time :       2021/02/23 13:33
# @Author :     Yuanyy
# @File :       3_IntegrateSingleRF.py
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
DIDA = pd.read_table("DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From", "Abundance.sub", "PS_2DbJacSim", "BioGRIDPP", "EssgCom"]]
obbfile = pd.read_table("Test_Results.txt")
# negative
MD = pd.read_table("Training_MD_FV.txt", na_values=".")
LOF = pd.read_table("Training_LOF_FV.txt", na_values=".")
MDLOF = pd.read_table("Training_MDLOF_FV.txt", na_values=".")
Random = pd.read_table("Training_Random_FV.txt", na_values=".")
DIDA_NDI = pd.read_table("Training_DIDA_NDI_FV.txt", na_values=".")

# load the model from disk
ModelNum = [5,10,30,37,39,40,44,48,55,59,109,114,122,124,133,154,172,176,200]
ModelIndex = [x-1 for x in ModelNum]
ModelList = []
for i in ModelIndex:
    modelname = modelinput + "Model\\RF_finalized_model_" + str(i + 1) + ".mdl"
    model = pickle.load(open(modelname, 'rb'))
    ModelList.append(model)

# assign the weight using obb_scores
Test_obb = list(obbfile.iloc[ModelIndex, 1])
weight = [(Test_obb[i] / sum(Test_obb)) for i in range(len(Test_obb))]

# Predict on training set
Alltraining = pd.concat([DIDA, MD, LOF, MDLOF, Random, DIDA_NDI], axis=0, ignore_index=True)
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

# predict on test set
Testset = pd.read_table("Testcom_FV.txt", na_values=".")
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

