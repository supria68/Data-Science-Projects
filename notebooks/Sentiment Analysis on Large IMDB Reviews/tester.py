"""
This tester script checks if our machine learning model predicts the sentiments accurately or not!

Steps:
    1. Load the model from the pickle file
    2. Get the user input, preprocess it (using helper script) and vectorize using TF-IDF
    3. Check the model prediction on the result of step 2
        a. Counter keeps the count of positive words in step 3.
        b. If count > length of words in step 2, sentiment is positive; else
        negative

"""
import pickle
import math
from helper import preprocess


# Load the model from pkl files
f = open('svm_model.pkl', 'rb')
myfiles = pickle.load(f)
f.close()

# Segregate the model and vectorizer
svc_model = myfiles[0]
vectorizer = myfiles[1]

# Perform prediction
print("\n\033[1m\t\tMovie Review's Sentiment Analysis\033[0m\n")
while True:
    count = 0 # This keeps the count of positive sentiments / word
    sentence = input("\n\033[93mPlease enter the review to get the sentiment evaluated. Enter \"exit\" to quit.\033[0m\n")
    if sentence == "exit":
        print("\033[93mexit program ...\033[0m\n")
        break
    else:
        input_features = preprocess(sentence)
        input_features = vectorizer.transform(input_features)
        prediction = svc_model.predict(input_features)
        for i in prediction:
            if i == 1:
                count += 1
        if count > math.ceil(len(prediction)/2):
            print("---- \033[92mPositive Review\033[0m\n")
        else:
            print("---- \033[91mNegative Review\033[0m\n")
