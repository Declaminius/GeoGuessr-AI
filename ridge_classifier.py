import numpy as np
import matplotlib.pyplot as plt

def sample_data(ds, sample_size):
     # Generate fresh training samples
    sample = ds.take(sample_size)
    images = np.array([x for (x, y) in sample.as_numpy_iterator()]).reshape((sample_size,-1))
    labels = np.array([y for (x, y) in sample.as_numpy_iterator()])
    return images, labels


def calculate_accuracy(regressor, images, labels):
    predicted_labels = regressor.predict(images)
    prediction_results = (predicted_labels == labels)
    print(f"{sum(prediction_results)} out of {len(prediction_results)} correctly classified.")
    return sum(prediction_results)/len(prediction_results)

def evaluate_regressor(regressor, sample_size, train_ds, val_ds):
    
    train_images, train_labels = sample_data(train_ds, sample_size)
    val_images, val_labels = sample_data(val_ds, sample_size)
    
    # Fit the regressor
    regressor.fit(train_images, train_labels)
    
    # Calculate the accuracy on the training data
    print("Training data:")
    train_accuracy = calculate_accuracy(regressor, train_images, train_labels)
    
    # Calculate the accuracy on the validation data
    print("Validation data:")
    val_accuracy = calculate_accuracy(regressor, val_images, val_labels)
    return train_accuracy, val_accuracy

def plot_accuracy(accuracy_array, title = None):
    mean = accuracy_array.mean(axis = 0)
    std = accuracy_array.std(axis = 0)
    xlabels = ["Training accuracy", "Validation accuracy"]
    plt.bar(xlabels, mean, yerr = std, align='center', alpha=0.5, ecolor='black', capsize=10)
    plt.axhline(0.5, linestyle = "dotted", color = "black")
    plt.title(title)