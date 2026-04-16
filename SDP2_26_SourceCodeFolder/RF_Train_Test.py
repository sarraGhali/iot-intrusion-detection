import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Separate features (X) and target variable (y)
X = df.drop(['Attack_label'], axis=1)
y = df['Attack_label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest model
rf_model = RandomForestClassifier(n_estimators=1, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Make predictions on the training set
y_train_pred = rf_model.predict(X_train)
# Make predictions on the testing set
y_test_pred = rf_model.predict(X_test)

# Evaluate the model on training data
train_accuracy = accuracy_score(y_train, y_train_pred)
train_conf_matrix = confusion_matrix(y_train, y_train_pred)
train_classification_rep = classification_report(y_train, y_train_pred)

# Extract TP, TN, FP, and FN from the training confusion matrix
train_TN, train_FP, train_FN, train_TP = train_conf_matrix.ravel()

# Display the results for training
print("\nTraining Confusion Matrix:")
print(train_conf_matrix)
print(f"True Positives (TP): {train_TP}\n")
print(f"True Negatives (TN): {train_TN}\n")
print(f"False Positives (FP): {train_FP}\n")
print(f"False Negatives (FN): {train_FN}\n")
print(f"Training Accuracy: {train_accuracy:.4f}\n")
print("Training Classification Report:")
print(train_classification_rep)

# Evaluate the model on testing data
test_accuracy = accuracy_score(y_test, y_test_pred)
test_conf_matrix = confusion_matrix(y_test, y_test_pred)
test_classification_rep = classification_report(y_test, y_test_pred)

# Extract TP, TN, FP, and FN from the testing confusion matrix
test_TN, test_FP, test_FN, test_TP = test_conf_matrix.ravel()

# Display the results for testing
print("\nTesting Confusion Matrix:")
print(test_conf_matrix)
print(f"True Positives (TP): {test_TP}\n")
print(f"True Negatives (TN): {test_TN}\n")
print(f"False Positives (FP): {test_FP}\n")
print(f"False Negatives (FN): {test_FN}\n")
print(f"Testing Accuracy: {test_accuracy:.4f}\n")
print("Testing Classification Report:")
print(test_classification_rep)