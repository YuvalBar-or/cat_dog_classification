# -*- coding: utf-8 -*-
"""precepton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QipGqZj8L_3wOCfKYOZ8HoPq5E1_UrK3

*classification using KNN and SVM*

* project - classification between cat and dogs. 
* reason of choise: i wanted to see if a machine could differentiate between somthing so trivial for us 
* note about the data: in order to get a clean data set, in the correct sizes i used a data set from kaggle : "Cats and Dogs image classification".
link to the data set: https://www.kaggle.com/datasets/samuelcortinhas/cats-and-dogs-image-classification

imports:
"""

from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn import metrics
import cv2
import os
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler

"""connecting to the data base """

from google.colab import drive
drive.mount('/content/drive')

drive_path = "/content/drive/MyDrive/data"
if os.path.isdir(drive_path):
    print("Google Drive is currently mounted.")
else:
    print("Google Drive is not currently mounted.")

"""loading the data from google drive:
* the data is divided into 2 folders - train and test, each folder has an equal amount of dogs and cats pictures. the train set has 20 images, while the test set has 10 images


"""

# loading the dorectories
image_directory_cats = "/content/drive/MyDrive/data/train/cats"
image_directory_dogs = "/content/drive/MyDrive/data/train/dogs"

## printing:

files = os.listdir(image_directory_cats)
# Select the first image file
first_image_file = files[0]
# Construct the full path to the image file
image_path = os.path.join(image_directory_cats,  first_image_file)
# Load the image using cv2.imread()
image = cv2.imread(image_path)
# Convert the image from BGR to RGB color format
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Display the image using matplotlib
plt.imshow(image_rgb)
plt.show()


files = os.listdir(image_directory_dogs)
# Select the first image file
first_image_file = files[1]
# Construct the full path to the image file
image_path = os.path.join(image_directory_dogs,  first_image_file)
# Load the image using cv2.imread()
image = cv2.imread(image_path)
# Convert the image from BGR to RGB color format
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Display the image using matplotlib
plt.imshow(image_rgb)
plt.show()

"""appling the avg rgb fucntion:
* The average_rgb function uses NumPy's array operations to calculate the average RGB values of an image. It does this by averaging the RGB values of all pixels in the image. This provides a single representative color that represents the average color of the entire image.

* thia function returns for each image an array.

"""

def average_rgb(image_path):
    try:
        # Load image using cv2.imread()
        image = cv2.imread(image_path)
        if image is None:
            print(f"Unable to load image: {image_path}")
            return None
        # Split image into RGB channels
        r, g, b = cv2.split(image)
        # Calculate mean values for each channel
        r_mean = np.mean(r)
        g_mean = np.mean(g)
        b_mean = np.mean(b)
        # Return average RGB values as an array
        return np.array([r_mean, g_mean, b_mean])
    except Exception as e:
        print(f"Error processing image: {image_path}")
        print(str(e))
        return None

# printing the rb stats just to make sure all the images go through 

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "cats rgb stats")

for image in os.listdir(image_directory_cats):
    image_path = os.path.join(image_directory_cats, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        avg_rgb = average_rgb(image_path)
        print(avg_rgb)
    else:
        print(f"Skipping non-image file: {image_path}")

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "dogs rgb stats")

for image in os.listdir(image_directory_dogs):
    image_path = os.path.join(image_directory_dogs, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        avg_rgb = average_rgb(image_path)
        print(avg_rgb)
    else:
        print(f"Skipping non-image file: {image_path}")

train_img =[]
train_labels = []

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "cats rgb stats")

for image in os.listdir(image_directory_cats):
    image_path = os.path.join(image_directory_cats, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        train_img.append(average_rgb(image_path))
        train_labels.append("cats")
        print(train_img)
        print(train_labels)
    else:
        print(f"Skipping non-image file: {image_path}")

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "dogs rgb stats")

for image in os.listdir(image_directory_dogs):
    image_path = os.path.join(image_directory_dogs, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        train_img.append(average_rgb(image_path))
        train_labels.append("dogs")
        print(train_img)
        print(train_labels)
    else:
        print(f"Skipping non-image file: {image_path}")

"""loading the test set:
* using the same methods as earlier 
"""

image_directory_test_cats = "/content/drive/MyDrive/data/test/cats"
image_directory_test_dogs = "/content/drive/MyDrive/data/test/dogs"

test_img =[]
test_labels = []


# printing the rb stats just to make sure all the images go through 

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "cats rgb stats")

for image in os.listdir(image_directory_test_cats):
    image_path = os.path.join(image_directory_test_cats, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        test_img.append (average_rgb(image_path))
        test_labels.append ("cats")
        print(test_img)
        print (test_labels)
   
    else:
        print(f"Skipping non-image file: {image_path}")

print ("-----------------------------------------------")
print ("-----------------------------------------------")
print( "dogs rgb stats")

for image in os.listdir(image_directory_test_dogs):
    image_path = os.path.join(image_directory_test_dogs, image)
    if not os.path.isfile(image_path):
        print(f"Image not found: {image_path}")
        continue

    if image_path.endswith(('.jpg', '.jpeg', '.png')):  # Check if the file is an image
        test_img.append (average_rgb(image_path))
        test_labels.append ("dogs")
        print(test_img)
        print (test_labels)
    else:
        print(f"Skipping non-image file: {image_path}")

"""visualize the data:
* using matplotlib
* Creating a plot graph to put the points - The graph represents a relationship between two colors.
* The graph is a visual aid to see if the images work, how they are separated into types and where the test images are located
"""

image_directory_test_cats = "/content/drive/MyDrive/data/test/cats"
image_directory_test_dogs = "/content/drive/MyDrive/data/test/dogs"

def scatter_plot_images(image_directory):
    image_files = os.listdir(image_directory)
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        try:
            avg_rgb = average_rgb(image_path)
            r, g, b = avg_rgb
            plt.scatter(r, g, c='red', marker='o')
            plt.scatter(r, b, c='green', marker='o')
            plt.scatter(g, b, c='blue', marker='o')
        except:
            print(f"Failed to process image: {image_path}")
    
    plt.xlabel('Red')
    plt.ylabel('Green')
    plt.title('Scatter Plot of RGB Colors')
    plt.show()

print ("---------------------------")
print ("---------------------------")
print ("cats stats")

if not os.path.exists(image_directory_test_cats):
    print(f"Directory not found: {image_directory_test_cats}")
else:
    scatter_plot_images(image_directory_test_cats)


print ("---------------------------")
print ("---------------------------")
print ("dogs stats")
if not os.path.exists(image_directory_test_dogs):
    print(f"Directory not found: {image_directory_test_dogs}")
else:
    scatter_plot_images(image_directory_test_dogs)

"""KNN:
* the main fucntions- knn and accuracy score 
"""

def knn_classify(train_img, train_labels, test_img, k):
    distances = []

    for test_sample in test_img:
        distances_per_sample = []
        
        for train_sample, train_label in zip(train_img, train_labels):
            distance = np.linalg.norm(np.array(train_sample) - np.array(test_sample))
            distances_per_sample.append((distance, train_label))
        
        distances_per_sample.sort(key=lambda x: x[0])
        k_nearest_neighbors = distances_per_sample[:k]
        
        distances.append(k_nearest_neighbors)
    
    predicted_labels = []
    for neighbors in distances:
        labels = [label for _, label in neighbors]
        predicted_label = max(set(labels), key=labels.count)
        predicted_labels.append(predicted_label)
    
    return predicted_labels

def calculate_accuracy(true_labels, predicted_labels):
    correct = sum(1 for true, predicted in zip(true_labels, predicted_labels) if true == predicted)
    accuracy = (correct / len(true_labels)) * 100
    return accuracy

"""* k = 3 - """

k = 3  # Number of nearest neighbors to consider

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, k)

# Calculate accuracy
accuracy = calculate_accuracy(test_labels, predicted_labels)

# Print the results
for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")

"""* k =5 - """

k = 5  # Number of nearest neighbors to consider

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, k)

# True labels for the test images (replace with your actual true labels)
true_labels = ["cats", "dogs", "cats", "dogs"]

# Calculate accuracy
accuracy = calculate_accuracy(true_labels, predicted_labels)

# Print the results
for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")

"""* k= 7 - """

k = 7  # Number of nearest neighbors to consider

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, k)

# True labels for the test images (replace with your actual true labels)
true_labels = ["cats", "dogs", "cats", "dogs"]

# Calculate accuracy
accuracy = calculate_accuracy(true_labels, predicted_labels)

# Print the results
for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")

"""confusion matrix

* k=3 -
"""

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, 3)
# True labels for the test images
actual_labels = test_labels
# Create the confusion matrix
cmatrix = confusion_matrix(actual_labels, predicted_labels)
# Create the ConfusionMatrixDisplay object
cm_display = ConfusionMatrixDisplay(confusion_matrix=cmatrix, display_labels=["cats", "dogs"])
# Plot the confusion matrix
cm_display.plot(cmap='Blues')
plt.title(f"Confusion Matrix (k = {3})")
plt.show()

"""* k= 5 -"""

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, 5)
# True labels for the test images
actual_labels = test_labels
# Create the confusion matrix
cmatrix = confusion_matrix(actual_labels, predicted_labels)
# Create the ConfusionMatrixDisplay object
cm_display = ConfusionMatrixDisplay(confusion_matrix=cmatrix, display_labels=["cats", "dogs"])
# Plot the confusion matrix
cm_display.plot(cmap='Blues')
plt.title(f"Confusion Matrix (k = {5})")
plt.show()

"""* k =7 - """

# Perform KNN classification
predicted_labels = knn_classify(train_img, train_labels, test_img, 7)
# True labels for the test images
actual_labels = test_labels
# Create the confusion matrix
cmatrix = confusion_matrix(actual_labels, predicted_labels)
# Create the ConfusionMatrixDisplay object
cm_display = ConfusionMatrixDisplay(confusion_matrix=cmatrix, display_labels=["cats", "dogs"])
# Plot the confusion matrix
cm_display.plot(cmap='Blues')
plt.title(f"Confusion Matrix (k = {7})")
plt.show()

final_answer = max(predicted_labels, key=predicted_labels.count)
print("Final Answer:", final_answer)

"""svm:

* c = 0.01 -
"""

# Convert the test_img and test_labels to NumPy arrays
test_img_array = np.array(test_img)
test_labels_array = np.array(test_labels)

# Convert the train_img and train_labels to NumPy arrays
train_img_array = np.array(train_img)
train_labels_array = np.array(train_labels)

# Concatenate the train_img_array and test_img_array
features = np.concatenate((train_img_array, test_img_array), axis=0)

# Encode the labels as numeric values
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(train_labels + test_labels)

# Add an extra feature with a constant value
features_with_extra = np.c_[features, np.ones(len(features))]

# Create an SVM classifier with a linear kernel
svm_classifier = SVC(kernel="linear", C=0.01)

# Train the classifier on the training data
svm_classifier.fit(features_with_extra, labels_encoded)

# Scatter plot of training data points
plt.scatter(features[:len(train_img_array), 0], features[:len(train_img_array), 1], color="red", label="Training Data")

# Scatter plot of test data points
plt.scatter(features[len(train_img_array):, 0], features[len(train_img_array):, 1], color="blue", label="Test Data")

# Get current axis limits
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Create meshgrid for decision boundary plot
xx = np.linspace(xlim[0], xlim[1], 100)
yy = np.linspace(ylim[0], ylim[1], 100)
XX, YY = np.meshgrid(xx, yy)
X_test = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.ravel().shape), np.ones(XX.ravel().shape)]  # Combine XX, YY, and two constant features

# Predict the labels for the meshgrid points
Z = svm_classifier.predict(X_test)

# Reshape the predicted labels to match the shape of XX and YY
Z = Z.reshape(XX.shape)

for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")


# Plot the decision boundary
plt.contourf(XX, YY, Z, alpha=0.5, cmap='viridis')

# Set labels and title
plt.xlabel("cats")
plt.ylabel("dogs")
plt.title("Scatter Matrix with Decision Boundary")
plt.legend()

# Show the plot
plt.show()

"""* c = 0.1 - """

# Convert the test_img and test_labels to NumPy arrays
test_img_array = np.array(test_img)
test_labels_array = np.array(test_labels)

# Convert the train_img and train_labels to NumPy arrays
train_img_array = np.array(train_img)
train_labels_array = np.array(train_labels)

# Concatenate the train_img_array and test_img_array
features = np.concatenate((train_img_array, test_img_array), axis=0)

# Encode the labels as numeric values
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(train_labels + test_labels)

# Add an extra feature with a constant value
features_with_extra = np.c_[features, np.ones(len(features))]

# Create an SVM classifier with a linear kernel
svm_classifier = SVC(kernel="linear", C=0.1)

# Train the classifier on the training data
svm_classifier.fit(features_with_extra, labels_encoded)

# Scatter plot of training data points
plt.scatter(features[:len(train_img_array), 0], features[:len(train_img_array), 1], color="red", label="Training Data")

# Scatter plot of test data points
plt.scatter(features[len(train_img_array):, 0], features[len(train_img_array):, 1], color="blue", label="Test Data")

# Get current axis limits
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Create meshgrid for decision boundary plot
xx = np.linspace(xlim[0], xlim[1], 100)
yy = np.linspace(ylim[0], ylim[1], 100)
XX, YY = np.meshgrid(xx, yy)
X_test = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.ravel().shape), np.ones(XX.ravel().shape)]  # Combine XX, YY, and two constant features

# Predict the labels for the meshgrid points
Z = svm_classifier.predict(X_test)

# Reshape the predicted labels to match the shape of XX and YY
Z = Z.reshape(XX.shape)

for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")


# Plot the decision boundary
plt.contourf(XX, YY, Z, alpha=0.5, cmap='viridis')

# Set labels and title
plt.xlabel("cats")
plt.ylabel("dogs")
plt.title("Scatter Matrix with Decision Boundary")
plt.legend()

# Show the plot
plt.show()

"""* c = 1.0 - """

# Convert the test_img and test_labels to NumPy arrays
test_img_array = np.array(test_img)
test_labels_array = np.array(test_labels)

# Convert the train_img and train_labels to NumPy arrays
train_img_array = np.array(train_img)
train_labels_array = np.array(train_labels)

# Concatenate the train_img_array and test_img_array
features = np.concatenate((train_img_array, test_img_array), axis=0)

# Encode the labels as numeric values
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(train_labels + test_labels)

# Add an extra feature with a constant value
features_with_extra = np.c_[features, np.ones(len(features))]

# Create an SVM classifier with a linear kernel
svm_classifier = SVC(kernel="linear", C=1.0)

# Train the classifier on the training data
svm_classifier.fit(features_with_extra, labels_encoded)

# Scatter plot of training data points
plt.scatter(features[:len(train_img_array), 0], features[:len(train_img_array), 1], color="red", label="Training Data")

# Scatter plot of test data points
plt.scatter(features[len(train_img_array):, 0], features[len(train_img_array):, 1], color="blue", label="Test Data")

# Get current axis limits
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Create meshgrid for decision boundary plot
xx = np.linspace(xlim[0], xlim[1], 100)
yy = np.linspace(ylim[0], ylim[1], 100)
XX, YY = np.meshgrid(xx, yy)
X_test = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.ravel().shape), np.ones(XX.ravel().shape)]  # Combine XX, YY, and two constant features

# Predict the labels for the meshgrid points
Z = svm_classifier.predict(X_test)

# Reshape the predicted labels to match the shape of XX and YY
Z = Z.reshape(XX.shape)

for i, result in enumerate(predicted_labels):
    print(f"Test image {i+1}: {result}")

print(f"Accuracy: {accuracy:.2f}%")


# Plot the decision boundary
plt.contourf(XX, YY, Z, alpha=0.5, cmap='viridis')

# Set labels and title
plt.xlabel("cats")
plt.ylabel("dogs")
plt.title("Scatter Matrix with Decision Boundary")
plt.legend()

# Show the plot
plt.show()

"""confusion matrix: """

# Add the constant feature to test_img_array
test_img_array_with_extra = np.c_[test_img_array, np.ones(len(test_img_array))]
# Predict labels for the test data
predicted_labels_encoded = svm_classifier.predict(test_img_array_with_extra)
predicted_labels = label_encoder.inverse_transform(predicted_labels_encoded)
# Create a confusion matrix
confusion_mat = confusion_matrix(test_labels_array, predicted_labels)
# Create the ConfusionMatrixDisplay object
cm_display = ConfusionMatrixDisplay(confusion_matrix=confusion_mat, display_labels=label_encoder.classes_)
# Plot the confusion matrix
cm_display.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

"""preceptron:
* the main functions:

* learning rate = 100 -
"""

def perceptron_predict(w, b, x):
    output = 0
    for i in range(len(w)):
        output += w[i] * x[i]
    output += b
    if output > 0:
        return "cats"
    else:
        return "dogs"

def perceptron_fit(featuresT, labelT, learning_rate=0.1, n_epochs=50):
    n_exmp, n_feat = featuresT.shape
    w = np.ones((n_feat))
    b = 1
    n_errors = 0
    for _ in range(n_epochs):
        for i in range(n_exmp):
            x = featuresT[i]
            y = labelT[i]
            predict = perceptron_predict(w, b, x)
            if y == "cats" and predict == "dogs":
                n_errors += 1
                for j in range(len(w)):
                    w[j] += learning_rate * x[j]
                b += learning_rate
            elif y == "dogs" and predict == "cats":
                n_errors += 1
                for j in range(len(w)):
                    w[j] -= learning_rate * x[j]
                b -= learning_rate
        if n_errors == 0:
            break
    return w, b

weights, bias = perceptron_fit(np.array(train_img), np.array(train_labels), learning_rate=0.1, n_epochs=50)

perceptron_results = []
for i in range(len(test_img)):
    if ((weights[0] * test_img[i][0] + weights[1] * test_img[i][1] + weights[2] * test_img[i][2] + bias) > 0):
        perceptron_results.append("cats")
    else:
        perceptron_results.append("dogs")

actual = test_labels
predicted = perceptron_results

confusion_matrix = metrics.confusion_matrix(actual, predicted) 
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=["dog", "cat"])
cm_display.plot(cmap='magma')
plt.show()

accuracy = metrics.accuracy_score(actual, predicted)
print(f"Accuracy: {accuracy * 100:.2f}%")

def plot_perceptron_decision_boundary(train_img, train_labels, weights, bias):
    train_img_array = np.array(train_img)
    colors = ['red' if label == 'dogs' else 'blue' for label in train_labels]

    for i in range(len(train_img_array)):
        x = train_img_array[i][0]
        y = train_img_array[i][2]
        plt.scatter(x, y, color=colors[i])

    plt.title("Red vs Blue")
    plt.ylabel("Blue")
    plt.xlabel("Red")

    x0 = np.min(train_img_array[:, 0])
    x1 = np.max(train_img_array[:, 0])
    y0 = -(x0 * weights[0] + bias) / weights[1]
    y1 = -(x1 * weights[0] + bias) / weights[1]
    plt.plot([x0, x1], [y0, y1])

    plt.show()

# train_img - training input data points
# train_labels - training labels
# weights - weights of the perceptron model
# bias - bias of the perceptron model

weights = np.array([1, -1])
bias = 1

plot_perceptron_decision_boundary(train_img, train_labels, weights, bias)
print(weights)
print(bias)

"""* learning rate = 1.0 -"""

def perceptron_predict(w, b, x):
    output = 0
    for i in range(len(w)):
        output += w[i] * x[i]
    output += b
    if output > 0:
        return "cats"
    else:
        return "dogs"

def perceptron_fit(featuresT, labelT, learning_rate=0.1, n_epochs=50):
    n_exmp, n_feat = featuresT.shape
    w = np.ones((n_feat))
    b = 1
    n_errors = 0
    for _ in range(n_epochs):
        for i in range(n_exmp):
            x = featuresT[i]
            y = labelT[i]
            predict = perceptron_predict(w, b, x)
            if y == "cats" and predict == "dogs":
                n_errors += 1
                for j in range(len(w)):
                    w[j] += learning_rate * x[j]
                b += learning_rate
            elif y == "dogs" and predict == "cats":
                n_errors += 1
                for j in range(len(w)):
                    w[j] -= learning_rate * x[j]
                b -= learning_rate
        if n_errors == 0:
            break
    return w, b

weights, bias = perceptron_fit(np.array(train_img), np.array(train_labels), learning_rate=0.1, n_epochs=50)

perceptron_results = []
for i in range(len(test_img)):
    if ((weights[0] * test_img[i][0] + weights[1] * test_img[i][1] + weights[2] * test_img[i][2] + bias) > 0):
        perceptron_results.append("cats")
    else:
        perceptron_results.append("dogs")

actual = test_labels
predicted = perceptron_results

confusion_matrix = metrics.confusion_matrix(actual, predicted) 
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=["dog", "cat"])
cm_display.plot(cmap='magma')
plt.show()

accuracy = metrics.accuracy_score(actual, predicted)
print(f"Accuracy: {accuracy * 100:.2f}%")

def plot_perceptron_decision_boundary(train_img, train_labels, weights, bias):
    train_img_array = np.array(train_img)
    colors = ['red' if label == 'dogs' else 'blue' for label in train_labels]

    for i in range(len(train_img_array)):
        x = train_img_array[i][0]
        y = train_img_array[i][2]
        plt.scatter(x, y, color=colors[i])

    plt.title("Red vs Blue")
    plt.ylabel("Blue")
    plt.xlabel("Red")

    x0 = np.min(train_img_array[:, 0])
    x1 = np.max(train_img_array[:, 0])
    y0 = -(x0 * weights[0] + bias) / weights[1]
    y1 = -(x1 * weights[0] + bias) / weights[1]
    plt.plot([x0, x1], [y0, y1])

    plt.show()

# train_img - training input data points
# train_labels - training labels
# weights - weights of the perceptron model
# bias - bias of the perceptron model

weights = np.array([1, -1])
bias = 1

plot_perceptron_decision_boundary(train_img, train_labels, weights, bias)
print(weights)
print(bias)

"""* learning rate = 0.001 - """

def perceptron_predict(w, b, x):
    output = 0
    for i in range(len(w)):
        output += w[i] * x[i]
    output += b
    if output > 0:
        return "cats"
    else:
        return "dogs"

def perceptron_fit(featuresT, labelT, learning_rate=0.1, n_epochs=50):
    n_exmp, n_feat = featuresT.shape
    w = np.ones((n_feat))
    b = 1
    n_errors = 0
    for _ in range(n_epochs):
        for i in range(n_exmp):
            x = featuresT[i]
            y = labelT[i]
            predict = perceptron_predict(w, b, x)
            if y == "cats" and predict == "dogs":
                n_errors += 1
                for j in range(len(w)):
                    w[j] += learning_rate * x[j]
                b += learning_rate
            elif y == "dogs" and predict == "cats":
                n_errors += 1
                for j in range(len(w)):
                    w[j] -= learning_rate * x[j]
                b -= learning_rate
        if n_errors == 0:
            break
    return w, b

weights, bias = perceptron_fit(np.array(train_img), np.array(train_labels), learning_rate=0.1, n_epochs=50)


perceptron_results = []
for i in range(len(test_img)):
    if ((weights[0] * test_img[i][0] + weights[1] * test_img[i][1] + weights[2] * test_img[i][2] + bias) > 0):
        perceptron_results.append("cats")
    else:
        perceptron_results.append("dogs")

actual = test_labels
predicted = perceptron_results

confusion_matrix = metrics.confusion_matrix(actual, predicted) 
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=["dog", "cat"])
cm_display.plot(cmap='magma')
plt.show()

accuracy = metrics.accuracy_score(actual, predicted)
print(f"Accuracy: {accuracy * 100:.2f}%")

def plot_perceptron_decision_boundary(train_img, train_labels, weights, bias):
    train_img_array = np.array(train_img)
    colors = ['red' if label == 'dogs' else 'blue' for label in train_labels]

    for i in range(len(train_img_array)):
        x = train_img_array[i][0]
        y = train_img_array[i][2]
        plt.scatter(x, y, color=colors[i])

    plt.title("Red vs Blue")
    plt.ylabel("Blue")
    plt.xlabel("Red")

    x0 = np.min(train_img_array[:, 0])
    x1 = np.max(train_img_array[:, 0])
    y0 = -(x0 * weights[0] + bias) / weights[1]
    y1 = -(x1 * weights[0] + bias) / weights[1]
    plt.plot([x0, x1], [y0, y1])

    plt.show()

# train_img - training input data points
# train_labels - training labels
# weights - weights of the perceptron model
# bias - bias of the perceptron model

weights = np.array([1, -1])
bias = 1

plot_perceptron_decision_boundary(train_img, train_labels, weights, bias)
print(weights)
print(bias)

"""explanation for results:

The perceptron algorithm, being a linear classifier, has limitations in accurately classifying all types of data. Specifically, when the data is not linearly separable, the perceptron model's accuracy can be limited.
"""