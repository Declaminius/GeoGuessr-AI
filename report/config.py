import tensorflow as tf
from tensorflow import keras
from tensorflow.data import AUTOTUNE

states_dict = {"Austria": ["Lower Austria", "Upper Austria", "Burgenland", "Styria", "Carinthia", "Salzburg", "Tyrol", "Vorarlberg", "Vienna"],\
                "Australia": ["australian_capital_territory", "tasmania", "northern_territory", "western_australia", "south_australia", "queensland", "victoria", "new_south_wales"],\
                "New Zealand": ["West Coast", "Marlborough", "Gisborne", "Nelson", "Tasman", "Southland", "Taranaki", "Hawke's Bay", "Northland", "Otago", "Manawatū-Whanganui", "Bay of Plenty", "Waikato", "Wellington", "Canterbury", "Auckland"],\
                "Slovakia": ["Region of Bratislava", "Nitra", "Trnava", "Trencin", "Kosice", "Region of Banska Bystrica", "Presov", "Zilina"],\
                "Czechia": ["Northwest", "Southwest", "Central Bohemia", "Prague", "Northeast", "Southeast", "Central Moravia", "Moravia-Silesia"]
                }


highway_filter = '["highway"~"motorway|trunk|primary|secondary"]'
highway_filter_pyrosm = {"highway": ["motorway", "trunk", "primary", "secondary"]}

batch_size = 32


def standardize_image(image, label):
    mean = tf.reduce_mean(image)
    std = tf.math.reduce_std(image)
    standardized_image = tf.map_fn(lambda x: (x - mean)/std, image)
    return (standardized_image, label)

def create_standardized_dataset(image_size, image_dir, class_names):
    train_ds, val_ds = keras.utils.image_dataset_from_directory(
        image_dir,
        validation_split=0.2,
        labels="inferred",
        class_names = class_names,
        subset="both",
        seed = 0,
        batch_size = batch_size,
        crop_to_aspect_ratio=True,
        image_size=(image_size, image_size))
    
    train_ds = train_ds.map(standardize_image)
    val_ds = val_ds.map(standardize_image)

    train_ds = train_ds.prefetch(buffer_size = AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size = AUTOTUNE)

    return train_ds, val_ds


train_ds, val_ds = create_standardized_dataset(image_size = 256, image_dir = "../images", class_names = ["Austria","Australia"])
train_ds32, val_ds32 = create_standardized_dataset(image_size = 32, image_dir = "../images", class_names = ["Austria","Australia"])
train_ds_multinomial, val_ds_multinomial = create_standardized_dataset(image_size = 256, 
                                                                       image_dir = "../images_multinomial", 
                                                                       class_names = ["Australia", "Austria", "Czechia", "New Zealand", "Slovakia"])

imagenet_ds = keras.utils.image_dataset_from_directory(
        "../images",
        labels="inferred",
        class_names=["Austria","Australia"],
        seed = 0,
        shuffle=False,
        batch_size = batch_size,
        crop_to_aspect_ratio=True,
        image_size=(224, 224))
imagenet_ds = imagenet_ds.map(standardize_image)
imagenet_ds = imagenet_ds.prefetch(buffer_size = AUTOTUNE)

model = keras.models.load_model('../neural_net')
multinomial_model = keras.models.load_model('../multinomial_neural_net')

baseline = tf.zeros(shape = ((256,256,3)))
baseline_prediction = model(tf.expand_dims(baseline, axis = 0))