import numpy as np
import matplotlib.pyplot as plt
from visualization_lib import Visualize, LinearTransform
import tensorflow as tf
import config

def rescale_image(image, new_min = 0, new_max = 1):
    image_min = np.min(image)
    image_max = np.max(image)
    if image_max - image_min > 0:
        image = (image*(new_max - new_min) + image_max*new_min - image_min*new_max)/(image_max - image_min)
    return image

def plot_accuracy(accuracy_array, title = None):
    mean = accuracy_array.mean(axis = 0)
    std = accuracy_array.std(axis = 0)
    xlabels = ["Training accuracy", "Validation accuracy"]
    plt.bar(xlabels, mean, yerr = std, align='center', alpha=0.5, ecolor='black', capsize=10)
    plt.axhline(0.5, linestyle = "dotted", color = "black")
    plt.title(title)

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


def plot_adversarial_image(image, adv_image, label, prediction, adv_prediction, eps, subfig):
    axl, axm, axr = subfig.subplots(nrows=1, ncols=3)
    plt.sca(axl)
    plot_image_with_confidence(image, label, prediction)

    plt.sca(axm)
    plt.imshow(rescale_image((adv_image - image)/eps))
    plt.text(-100, 128, f'+ {eps} ×', verticalalignment = 'top', rotation = 0)

    plt.sca(axr)
    plt.text(-50, 128, '=', verticalalignment = 'top', rotation = 0)
    plot_image_with_confidence(adv_image, label, adv_prediction[0])

def visualize_integrated_gradients(image, label, prediction, integrated_gradients):
    visual_attributions = Visualize(integrated_gradients, np.uint8(rescale_image(image,0,255)[0]), 
                                        polarity = "both", overlay = False, morphological_cleanup = True,
                                       clip_above_percentile=99, clip_below_percentile=0)

    plt.subplot(1,3,1)
    rescaled_image = rescale_image(image)
    plt.imshow(rescaled_image[0])
    if prediction > 0.5:
        if np.round(prediction) == label:
            plt.title(f"{100*prediction:.2f}\% confidence: Australia", color = "green")
        else:
            plt.title(f"{100*prediction:.2f}\% confidence: Australia", color = "red")
    else:
        if np.round(prediction) == label:
            plt.title(f"{100*(1-prediction):.2f}\% confidence: Austria", color = "green")
        else:
            plt.title(f"{100*(1-prediction):.2f}\% confidence: Austria", color = "red")

    plt.subplot(1,3,2)
    plt.imshow(np.uint8(visual_attributions))
    plt.title(f"sum of attributions: {np.sum(integrated_gradients):.2f}")

    plt.subplot(1,3,3)

    image = rescale_image(image,0,1)
    aggregated_attributions = LinearTransform(np.average(tf.math.abs(integrated_gradients), axis=2), clip_above_percentile=95,
                clip_below_percentile=50.0,
                low=0.2,
                plot_distribution=False)
    weighted_image = tf.repeat(tf.expand_dims(aggregated_attributions, axis = 2),3, axis = 2)*image
    plt.imshow(rescale_image(weighted_image)[0])
    plt.title(f"prediction - baseline_prediction: {(prediction - config.baseline_prediction[0,0]):.2f}")
    plt.tight_layout()