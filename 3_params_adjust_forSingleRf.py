#-*- coding = utf-8 -*-
# @Time :       2021/02/22 22:22
# @Author :     Yuanyy
# @File :       3_params_adjust_forSingleRf.py
# @Package :
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :


import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score, average_precision_score, recall_score, precision_score
from sklearn.model_selection import GridSearchCV    #导入网格搜索自动调参函数GridSearchCV
import warnings    #导入Python中的warnings模块
warnings.filterwarnings('ignore')

# input files
input = ""
# positive
DIDA = pd.read_table(input + "DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From", "Abundance.sub", "PS_2DbJacSim", "BioGRIDPP", "EssgCom"]]
# negative
DIDA_NDI = pd.read_table(input + "Training_DIDA_NDI_FV.txt", na_values=".")
Random = pd.read_table(input + "Training_Random_FV.txt", na_values=".")

# set the range of different paras
params_dict = {'n_estimators': list(range(250, 300, 5)), 'max_depth': list(range(12, 20, 2)),
          'min_samples_split': list(range(2, 5, 1)), 'min_samples_leaf': list(range(1, 4, 1)),
          'max_features': list(range(3, 10, 2))}

# generate seeds
random.seed(903904)
seted_seeds = random.sample(range(1000, 1000000), 200)
result_dict = {"seted_seeds": [], "n_estimators": [], "max_depth": [], "min_samples_split": [], "min_samples_leaf": [], "max_features": []}

for i in list(range(200)):
    print("Model " + str(i + 1))
    Training = pd.read_table(input + "TrainingSet/Trainingset" + str(i + 1) + ".txt", na_values=".")
    X, y = Training[features], Training["Class"]

    gsearch = GridSearchCV(estimator=RandomForestClassifier(), param_grid=params_dict, scoring='f1', cv=10, n_jobs=60)
    gsearch.fit(X, y)
    result_dict['seted_seeds'].append(seted_seeds[i])
    result_dict['n_estimators'].append(gsearch.best_params_["n_estimators"])
    result_dict['max_depth'].append(gsearch.best_params_["max_depth"])
    result_dict['min_samples_split'].append(gsearch.best_params_["min_samples_split"])
    result_dict['min_samples_leaf'].append(gsearch.best_params_["min_samples_leaf"])
    result_dict['max_features'].append(gsearch.best_params_["max_features"])

pd.DataFrame(result_dict).to_csv(input + "best_params.txt", sep="\t", index=False)
