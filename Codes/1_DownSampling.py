#-*- coding = utf-8 -*-
# @Time :       2021/02/23 12:00
# @Author :     Yuanyy
# @File :       1_DownSampling.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

# 导入所需资源
import random
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from Utils import *

# 导入文件
input = ""
output = ""
# positive
DIDA = pd.read_table(input + "DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From"]]
# negative
MD = pd.read_table("Training_MD_FV.txt", na_values=".")
LOF = pd.read_table("Training_LOF_FV.txt", na_values=".")
MDLOF = pd.read_table("Training_MDLOF_FV.txt", na_values=".")
Random = pd.read_table("Training_Random_FV.txt", na_values=".")
DIDA_NDI = pd.read_table("Training_DIDA_NDI_FV.txt", na_values=".")

# 生成随机数种子，用于欠采样
random.seed(903904)
seted_seeds = random.sample(range(1000, 1000000), 200)  # 生成不重复的随机数组用于后面的采样
# 导出seed列表
Seeds = open(output + "Seeds.txt", "a")
Seeds.write("Seeds" + "\n")
for n in list(range(200)):
    Seeds.write(str(seted_seeds[n]) + "\n")
Seeds.close()

# 开始欠采样
for i in list(range(200)):
    print(i+1)
    random.seed(seted_seeds[i])
    sample = random.sample(range(1000), 30)
    MDset = MD.iloc[sample, ]
    LOFset = LOF.iloc[sample, ]
    MDLOFset = MDLOF.iloc[sample, ]
    Randomset = Random.iloc[sample, ]
    DIDA_NDIset = DIDA_NDI.iloc[sample, ]
    Training = pd.concat([DIDA, MDset, LOFset, MDLOFset, Randomset, DIDA_NDIset], axis=0, ignore_index=True)
    Training.to_csv(output + "Trainingset" + str(i + 1) + ".txt", sep="\t", index=False)
