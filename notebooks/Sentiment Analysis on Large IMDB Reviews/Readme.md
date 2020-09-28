# Sentiment Analysis on Large IMDB Movie Reviews

This repository consists of files required to create and deploy a machine learning model for analysing sentiments on large IMDB movie reviews.

### Dataset:
Data[1] for this experiment is taken from [here](http://ai.stanford.edu/~amaas/data/sentiment/).
The core dataset contains 50,000 reviews split evenly into 25k train and 25k test sets. The overall distribution of labels is balanced (25k pos and 25k neg).

### Packages Required:
python, nltk, pickle, sklearn

### Files:
train.pkl, test.pkl -> These are the pickled training and testing data.  
helper.py, svm_model.py, tester.py -> python scripts for data gathering, processing, model creation and deployment
svm_model.pkl -> Machine Learning model for deployment

### Steps to Execute:
1. Git clone the repository
2. Run ```python3 tester.py```
3. Type your statements to analyze the sentiment or exit to quit.

### Results:


Machine Learning model has an accuracy of 87.26%



### Reference:
[1] [Learning Word Vectors for Sentiment Analysis - ACL Anthology](https://www.aclweb.org/anthology/P11-1015/)
