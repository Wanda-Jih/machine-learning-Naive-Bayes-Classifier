# Naive Bayes Classifier

Build Naive Bayes Classifier from scratch without using the library

### Description

This project is for the purpose of processing a speed dating data.
I need to do pre-processing first to remove the unneeded symbols from the table and then normalize the data. 
And then put the data into the created classifier to do the analysis.


### Steps for running this repo
1. Execute `preprocessing.py`

Output: `dating.csv` and the following result

2. Execute `2_1.py`

Output: `img/gender_attributes.jpg` and the following result


3. Execute `2_2.py`

Output : you will get six images which locate at `ima/`
* attractive_partner_success_rate.jpg
* ambition_partner_success_rate.jpg
* funny_partner_success_rate.jpg
* intelligence_parter_success_rate.jpg
* shared_interests_partner_success_rate.jpg
* sincere_partner_success_rate.jpg

4. Execute `deicretize.py`

Output : `dating-binned.csv` 

5. Execute `split.py`

Output : `trainingSet.csv` and `testSet.csv.`

6. Execute `5_1.py`

Output : 
```
Training Accuracy: 0.76
Testing Accuracy: 0.75
```

7. Execute `5_2.py`

Output : `img/(5_2)different_bins.jpg`

When you execute this code, it will take at least 10 minutes.

8. Execute `5_3.py`

Output : `img/(5_3)different_fraction.jpg`
