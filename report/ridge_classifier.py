import numpy as np
import matplotlib.pyplot as plt

def sample_data(ds, sample_size):
     # Generate fresh training samples
    sample = ds.take(sample_size)
    images = np.array([x for (x, y) in sample.as_numpy_iterator()]).reshape((sample_size,-1))
    labels = np.array([y for (x, y) in sample.as_numpy_iterator()])*2 - 1
    return images, labels


def calculate_accuracy(regressor, images, labels, printlines):
    predicted_labels = regressor.predict(images)
    prediction_results = (predicted_labels == labels)
    if printlines:
        print(f"{sum(prediction_results)} out of {len(prediction_results)} correctly classified.")
    return sum(prediction_results)/len(prediction_results)

def evaluate_regressor(regressor, sample_size, train_ds, val_ds, printlines = False):
    
    train_images, train_labels = sample_data(train_ds, sample_size)
    val_images, val_labels = sample_data(val_ds, sample_size)
    
    # Fit the regressor
    regressor.fit(train_images, train_labels)
    
    # Calculate the accuracy on the training data
    if printlines:
        print("Training data:")
    train_accuracy = calculate_accuracy(regressor, train_images, train_labels, printlines)
    
    # Calculate the accuracy on the validation data
    if printlines:
        print("Validation data:")
    val_accuracy = calculate_accuracy(regressor, val_images, val_labels, printlines)
    return train_accuracy, val_accuracy