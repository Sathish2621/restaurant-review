# -*- coding: utf-8 -*-
"""ReviewClassification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uSmyn_1bgu-mb5UJXJhWu5KlV0QwVJb4

# New Section

IMPORTING THE LIBRARIES
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from google.colab import drive
drive.mount('/content/drive')

"""Loading Datasets"""

# Load the dataset
df = pd.read_csv('/content/Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
print(df.head())

"""Text Preprocessing"""

# Download stopwords
nltk.download('stopwords')

# Initialize PorterStemmer
ps = PorterStemmer()

# List to store cleaned reviews
corpus = []

# Loop through each review
for i in range(len(df)):
    # Remove non-alphabetic characters
    review = re.sub('[^a-zA-Z]', ' ', df['Review'][i])
    # Convert to lowercase
    review = review.lower()
    # Split into words
    review = review.split()
    # Remove stopwords and perform stemming
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    # Join words back into a sentence
    review = ' '.join(review)
    # Append to corpus
    corpus.append(review)

print(corpus[:5])  # Check the first 5 cleaned reviews

"""Feature Processing"""

# Initialize CountVectorizer
cv = CountVectorizer(max_features=1500)  # Limit to 1500 most frequent words

# Fit and transform the corpus into a sparse matrix
X = cv.fit_transform(corpus).toarray()
y = df['Liked'].values

print(X.shape)  # Check the shape of the feature matrix

"""Splits the Dataset"""

# Split the data into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Train a Machine Learning Model"""

# Initialize the Naive Bayes classifier
classifier = GaussianNB()

# Train the model
classifier.fit(X_train, y_train)

""" Evaluate the Model"""

# Predict on the test set
y_pred = classifier.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

"""Test with New Reviews"""

# Function to predict sentiment
def predict_sentiment(review):
    # Preprocess the review
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    # Convert to feature vector
    review_vector = cv.transform([review]).toarray()
    # Predict sentiment
    prediction = classifier.predict(review_vector)
    return "Positive" if prediction[0] == 1 else "Negative"

# Test with a new review
new_review = "food is very tasty"
print("Predicted Sentiment:", predict_sentiment(new_review))