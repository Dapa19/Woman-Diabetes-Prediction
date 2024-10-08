# -*- coding: utf-8 -*-
"""Diabetes Prediction Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QbDMaNdHgAy6ctkeupGAaBVG9mXcXPKM
"""

# Commented out IPython magic to ensure Python compatibility.
#Import Library
# %matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#read dataset
diabetes_df = pd.read_csv('diabetes-dataset.csv')
diabetes_df.columns

diabetes_df.head()

#Show Data Dimension
print('Data DImension : {}'.format(diabetes_df.shape))

#Counting Outcome Classes
diabetes_df.groupby('Outcome').size()

#Displays data per factor based on outcome = 0

# Filter data
outcome_0_df = diabetes_df[diabetes_df['Outcome'] == 0]

outcome_0_df.hist(figsize=(9, 9))
plt.show()

#Displays data per factor based on outcome = 1

# Filter data
outcome_1_df = diabetes_df[diabetes_df['Outcome'] == 1]

outcome_1_df.hist(figsize=(9, 9))
plt.show()

"""# Clean Data"""

#Checking null values
diabetes_df.isnull().sum()
diabetes_df.isna().sum()

"""## Checking Outlier"""

# Search for data where blood pressure = 0
print("Data with Blood Pressure = 0 : ", diabetes_df[diabetes_df.BloodPressure == 0].shape[0])
print("\n", diabetes_df[diabetes_df.BloodPressure == 0].groupby('Outcome')['Age'].count())

# Search for data where glucose = 0
print("Data with Glucose = 0 : ", diabetes_df[diabetes_df.Glucose == 0].shape[0])

print("\n", diabetes_df[diabetes_df.Glucose == 0].groupby('Outcome')['Age'].count())

# Search for data where skin thickness = 0
print("Data with skin thickness = 0 : ", diabetes_df[diabetes_df.SkinThickness == 0].shape[0])
print("\n", diabetes_df[diabetes_df.SkinThickness == 0].groupby('Outcome')['Age'].count())

# Search for data where BMI = 0
print("Data with BMI = 0 : ", diabetes_df[diabetes_df.BMI == 0].shape[0])
print("\n", diabetes_df[diabetes_df.BMI == 0].groupby('Outcome')['Age'].count())

# Search for data where insulin = 0
print("Data with insulin = 0 : ", diabetes_df[diabetes_df.Insulin == 0].shape[0])
print("\n", diabetes_df[diabetes_df.Insulin == 0].groupby('Outcome')['Age'].count())

"""## Edit Data"""

# Cleaning the data
diabetes_mod = diabetes_df[(diabetes_df.BloodPressure != 0) & (diabetes_df.BMI != 0) & (diabetes_df.Glucose != 0)]
print(diabetes_mod.shape)

#Split the data
factor = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
       'BMI', 'DiabetesPedigreeFunction', 'Age']

X = diabetes_mod[factor]
y = diabetes_mod.Outcome

"""# Training Model"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

model = LogisticRegression(random_state=0)

#Split the Data
X_train, X_test, y_train, y_test = train_test_split(X,y,stratify=diabetes_mod.Outcome, random_state=0)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
train_data_scaled = sc.fit_transform(X_train)
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

model.fit(train_data_scaled, y_train)

X_test

# Predict the probabilities on the test set
y_pred_prob = model.predict_proba(X_test)[:, 1]

# Predict the binary outcome
y_pred = model.predict(X_test)

y_pred

y_pred_prob

#Prediction Test
model.predict([[2,100, 72, 25, 78, 30.0, 0.22, 19]])[0]

"""# Model Evaluation"""

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

precision = precision_score(y_test, y_pred)
print("Precision:", precision)

recall = recall_score(y_test, y_pred)
print("Recall:", recall)

f1 = f1_score(y_test, y_pred)
print("F1 Score:", f1)

print("Model Score:", model.score(X_test, y_test))

"""# Save ML Model"""

import joblib

joblib.dump(sc, 'scaler.pkl')

joblib.dump(model, 'diabetes_prediction.pkl')