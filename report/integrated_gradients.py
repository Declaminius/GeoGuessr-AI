import numpy as np
import tensorflow as tf
import config

def get_attributions(image, baseline, m):
    grads = np.zeros((m+1,32, 256,256,3))
    for i in range(m+1):
        current_sample = baseline + (image - baseline)*i/m
        with tf.GradientTape() as g:
            g.watch(current_sample)
            predicted_label = config.model(current_sample)

            grads[i] = g.gradient(target = predicted_label, sources = current_sample)

    avg_grads = np.average((grads[:-1] + grads[1:]) / 2.0, axis = 0)
    return avg_grads*(image-baseline)