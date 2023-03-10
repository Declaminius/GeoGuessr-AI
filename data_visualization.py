import numpy as np
import matplotlib.pyplot as plt

def rescale_image(image, new_min = 0, new_max = 1):
    image_min = np.min(image)
    image_max = np.max(image)
    if image_max - image_min > 0:
        image = (image*(new_max - new_min) + image_max*new_min - image_min*new_max)/(image_max - image_min)
    return image

def plot_image_with_confidence(image, label, prediction):
    plt.imshow(rescale_image(image.numpy()))
    plt.axis("off")
    if prediction > 0.5:
        if round(prediction) == label:
            plt.title(f"Australia: {100*prediction:.2f}\% confidence", size = 10, color = "green")
        else:
            plt.title(f"Australia: {100*prediction:.2f}\% confidence", size = 10, color = "darkred")
        
    elif prediction <= 0.5:
        if round(prediction) == label:
            plt.title(f"Austria: {100*(1-prediction):.2f}\% confidence", size = 10, color = "green")
        else:
            plt.title(f"Austria: {100*(1-prediction):.2f}\% confidence", size = 10, color = "darkred")
