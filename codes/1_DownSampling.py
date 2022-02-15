#-*- coding = utf-8 -*-
# @Time :       2021/02/23 12:00
# @Author :     Yuanyy
# @File :       1_DownSampling.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import random
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from Utils import *

input = "DIEP\\ML\\Trainingset\\"
output = "DIEP\\results\\"
# positive
DIDA = pd.read_table(input + "DIDAcom_FV.txt", na_values=".")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From"]]
# negative
DIDA_NDI = pd.read_table(input + "Training_DIDA_NDI_FV.txt", na_values=".")
Random = pd.read_table(input + "Training_Random_FV.txt", na_values=".")

# random seeds
random.seed(903904)
seted_seeds = random.sample(range(1000, 1000000), 200)
Seeds = open(output + "ModelPara\\Seeds.txt", "a")
Seeds.write("Seeds" + "\n")
for n in list(range(200)):
    Seeds.write(str(seted_seeds[n]) + "\n")
Seeds.close()

# Start down-sampling
for i in list(range(200)):
    print(i+1)
    random.seed(seted_seeds[i])
    sample1 = random.sample(range(1400), 50)
    sample2 = random.sample(range(1400), 50)
    DIDA_NDIset = DIDA_NDI.iloc[sample1, ]
    Randomset = Random.iloc[sample2, ]
    Training = pd.concat([DIDA, DIDA_NDIset, Randomset], axis=0, ignore_index=True)
    Training.to_csv(output + "Trainingset" + str(i + 1) + ".txt", sep="\t", index=False)
