import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import VarianceThreshold
import time
#['frame.time', 'ip.src_host', 'ip.dst_host', 'tcp.ack', 'tcp.ack_raw', 'tcp.connection.rst','tcp.connection.syn','tcp.flags.ack','tcp.dstport','tcp.seq', 'tcp.srcport', 'Attack_label']
# Record the start time
start_time = time.time()
# Separate features (X) and target variable (y)
X = df.drop(['Attack_label','tcp.connection.rst'], axis=1)
y = df['Attack_label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create an instance of VarianceThreshold
selector = VarianceThreshold()

# Fit and transform on the training set
X_train_scaled_no_const = selector.fit_transform(X_train_scaled)

# Transform the test set using the same selector
X_test_scaled_no_const = selector.transform(X_test_scaled)
# Create an SVM model (linear kernel)
svm_model = SVC(kernel='rbf', random_state=42)

# Train the SVM model
svm_model.fit(X_train_scaled_no_const, y_train)
# Record the end time
end_time = time.time()
# Make predictions on the training set
y_train_pred = svm_model.predict(X_train_scaled_no_const)
# Make predictions on the testing set
y_test_pred = svm_model.predict(X_test_scaled_no_const)

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
# Calculate the training time
training_time = end_time - start_time
# Print the training time
print("Training Time:", training_time, "seconds")

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