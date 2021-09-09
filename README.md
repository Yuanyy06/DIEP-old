# Digenic-Interaction-Effect-Predictor (DIEP)
Gene-gene interaction on the genome is increasingly being proven to play an important role in developing human diseases. However, conventional statistical genetic analyses on the interactions often suffer from a dimension burden on the entire genome. We proposed a framework to predict pathogenic gene pairs with digenic interaction effect based on the biological relatedness or similarity of the genes with an accurate machine-learning approach , named Digenic Interaction Effect Predictor. The digenic interaction potential scores between each two coding genes across the whole genome are available. DIEP reveals potential gene pairs with interactive effects and provides a valuable resource of genome-wide digenic interactions. It might substantially facilitate and motivate many genomic studies on the gene-gene interaction of human diseases.

# File Discription
## Datasets_S1-S6
The compressed file of 6 Supplementary Datasets with large file size. Due to the limited storage of Git LFS Data, this datasets are moved to our OneDrive, the download link is: https://mailsysueducn-my.sharepoint.com/:f:/g/personal/limiaoxin_mail_sysu_edu_cn/EjKo3l_HQcZEjHCeqJ9mDREBrtoJSVJjhlPjA1l9OGQGZg.

## Dataset_S7-CodingDIScores
The compressed file of Dataset S7-the Digenic interaction scores for each two coding genes across the whole genome. The compressed file is also moved to our OneDrive (https://mailsysueducn-my.sharepoint.com/:f:/g/personal/limiaoxin_mail_sysu_edu_cn/EjKo3l_HQcZEjHCeqJ9mDREBrtoJSVJjhlPjA1l9OGQGZg). There are two files in the directory after decompressing the (Dataset_S7-CodingDIScores.zip) file, including Coding_predict_fixed.txt.b and Coding_predict_fixed.txt.d for decoding the compressed file.

# Codes Discription
## Down-SamplingRF.py
Use the down-sampling technique for training individual classifiers with different sub-samples.

## transfer.jar
The pre-calculated digenic interaction potential scores between each two coding genes across the whole genome are available. transfer.jar is the self-defined software for decoding the compressed file of Dataset S6 and searching the digenic scores of specific gene pairs.  

### User manual
1.File requirements:  
Users need to download the required files from the web page, including the resource file (Dataset_S7-CodingDIScores.zip) and the java package (transfer.jar).

2.Decompress files:  
```unzip Dataset_S7-CodingDIScores.zip```  
>After decompressed, you will get two different files including a dictionary file (Coding_predict_fixed.d) and a binary zip file (Coding_predict_fixed.b).

3.Decode the binary zip file:  
```# [java -jar transfer.jar --decode inputFileName outputFileName]```  
```java -jar transfer.jar --decode Coding_predict_fixed Coding_predict_fixed```  
>If you didn't rename the files in CodingDIScores.tar.bz2, then the inputFileName should be "Coding_predict_fixed" (Without ".d" and ".b"). After decoding, you will get a file with size 3,828,259,574B (3.56G, Coding_predict_fixed.txt). This step will take about 10s.  

4.For help:   
```java -jar transfer.jar --read -help```  
```java -jar transfer.jar --decode -help```  

5.Searching  
Search the digenic interaction potential score for specific a gene pair:  
```java -jar transfer.jar --read Coding_predict_fixed -gn AGRN TAS1R3``` 
  
Search the digenic interaction potential scores with a gene list:  
```java -jar transfer.jar --read Coding_predict_fixed -gn AGRN TAS1R3 ARHGEF16 CCDC27 CHD5``` 
  
Set the column name:  
```java -jar transfer.jar --read Coding_predict_fixed -gn AGRN TAS1R3 --header Ga Gb Score``` 


