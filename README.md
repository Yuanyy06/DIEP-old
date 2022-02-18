# Digenic-Interaction-Effect-Predictor (DIEP)
Gene-gene interaction on the genome is increasingly being proven to play an important role in developing human diseases. However, conventional statistical genetic analyses on the interactions often suffer from a dimension burden on the entire genome. We proposed a framework to predict pathogenic gene pairs with digenic interaction effect based on the biological relatedness or similarity of the genes with an accurate machine-learning approach , named Digenic Interaction Effect Predictor. The digenic interaction potential scores between each two coding genes across the whole genome are available. DIEP reveals potential gene pairs with interactive effects and provides a valuable resource of genome-wide digenic interactions. It might substantially facilitate and motivate many genomic studies on the gene-gene interaction of human diseases.

# File Description
## ML
### Trainingset
All the training sets for model construction.

### Testset
All the test sets for model evaluation.

### Model
The selected 26 RF classifiers for ensemble.

## DATASETS
The Supplementary Datasets (S1-S8). Due to the limited storage of Git LFS Data, some datasets with large file size are moved to our OneDrive, the download link is: https://mailsysueducn-my.sharepoint.com/:f:/g/personal/limiaoxin_mail_sysu_edu_cn/EjKo3l_HQcZEjHCeqJ9mDREBrtoJSVJjhlPjA1l9OGQGZg?e=VWySpZ.

Dataset_S7-CodingDIScores
The compressed file of Dataset S7-the Digenic interaction scores for each two coding genes across the whole genome. The compressed file is also moved to our OneDrive (https://mailsysueducn-my.sharepoint.com/:f:/g/personal/limiaoxin_mail_sysu_edu_cn/EjKo3l_HQcZEjHCeqJ9mDREBrtoJSVJjhlPjA1l9OGQGZg?e=VWySpZ). There are two files in the directory after decompressing the (Dataset_S7-CodingDIScores.zip) file, including Coding_predict_fixed.txt.b and Coding_predict_fixed.txt.d for decoding the compressed file.

## TABLES
The Supplementary Tables (S5 and S6).

## CODES
1_DownSampling.py  
2_FeatureSelection.py  
3_params_adjust_forSingleRf.py  
4_DownSampleRF.py  
5_IntegrateSingleRF.py  
Use the down-sampling technique for training individual classifiers with different sub-samples, and integrate single classifiers for final prediction.

## transfer.jar
The pre-calculated digenic interaction potential scores between each two coding genes across the whole genome are available. transfer.jar is the self-defined software for decoding the compressed file of Dataset S6 and searching the digenic scores of specific gene pairs.  

## User manual
1.File requirements:  
Users need to download the required files from the web page, including the resource file (Dataset_S7-CodingDIScores.zip) and the java package (transfer.jar).

2.Decompress files:  
```unzip Dataset_S7-CodingDIScores.zip```  
>After decompressed, you will get two different files including a dictionary file (Coding_predict_fixed.d) and a binary zip file (Coding_predict_fixed.b).

3.Decode the binary zip file:  
```# [java -jar transfer.jar --decode inputFileName outputFileName]```  
```java -jar transfer.jar --decode Coding_predict_fixed.txt Coding_predict_fixed```  
>If you didn't rename the files in Dataset_S7-CodingDIScores.zip, then the inputFileName should be "Coding_predict_fixed.txt" (Without ".d" and ".b"). After decoding, you will get a file with size 3,828,259,574B (3.56G, Coding_predict_fixed.txt). This step will take about 10s.  

4.For help:   
```java -jar transfer.jar --read -help```  
```java -jar transfer.jar --decode -help```  

5.Searching  
Search the digenic interaction potential score for specific a gene pair:  
```java -jar transfer.jar --read Coding_predict_fixed.txt -gn AGRN TAS1R3``` 
  
Search the digenic interaction potential scores with a gene list:  
```java -jar transfer.jar --read Coding_predict_fixed.txt -gn AGRN TAS1R3 ARHGEF16 CCDC27 CHD5``` 
  
Set the column name:  
```java -jar transfer.jar --read Coding_predict_fixed.txt -gn AGRN TAS1R3 --header Ga Gb Score``` 


