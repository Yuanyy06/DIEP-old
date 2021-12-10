#-*- coding = utf-8 -*-
# @Time :       2021/02/23 12:00
# @Author :     Yuanyy
# @File :       1_DownSampling.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

# import
import random
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from Utils import *

# inport files
input = ""
output = ""
# positive
DIDA = pd.read_table(input + "Original\\DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From"]]
# negative
DIDA_NDI = pd.read_table(input + "Delt\\Training_DIDA_NDI_FV.txt", na_values=".")
Random = pd.read_table(input + "Delt\\Training_Random_FV.txt", na_values=".")

# generate seeds
random.seed(903904)
seted_seeds = random.sample(range(1000, 1000000), 200)  # 生成不重复的随机数组用于后面的采样
# output seeds
Seeds = open(output + "ModelPara\\Seeds.txt", "a")
Seeds.write("Seeds" + "\n")
for n in list(range(200)):
    Seeds.write(str(seted_seeds[n]) + "\n")
Seeds.close()

# start down-sampling
for i in list(range(200)):
    print(i+1)
    random.seed(seted_seeds[i])
    sample1 = random.sample(range(1400), 50)
    sample2 = random.sample(range(1400), 50)
    DIDA_NDIset = DIDA_NDI.iloc[sample1, ]
    Randomset = Random.iloc[sample2, ]
    Training = pd.concat([DIDA, DIDA_NDIset, Randomset], axis=0, ignore_index=True)
    Training.to_csv(output + "TrainingSet\\Trainingset" + str(i + 1) + ".txt", sep="\t", index=False)
