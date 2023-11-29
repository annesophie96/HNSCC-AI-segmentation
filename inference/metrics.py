import tensorflow as tf
from segmentation_models.metrics import IOUScore
from segmentation_models.losses import *

# Define a weighted categorical cross-entropy loss function with custom class weights.
# Class weights are applied to cater for class imbalance in the dataset.
# The zeroth class is weighted as 0 (usually representing a background class that might be ignored).
WCat = CategoricalCELoss(class_weights=[0, 1, 1, 1])

# Define the Intersection over Union (IoU) score as a metric for each class.
# The IoU score is a common evaluation metric for tasks like semantic segmentation.
metric = IOUScore()
IOUscore0 = IOUScore(class_indexes=0, name='IOU_Not_Annotated')  # IoU for the 'Not_Annotated' class
IOUscore1 = IOUScore(class_indexes=1, name='IOU_Tumor')  # IoU for the 'Tumor' class
IOUscore2 = IOUScore(class_indexes=2, name='IOU_Other')  # IoU for the 'Other' class
IOUscore3 = IOUScore(class_indexes=3, name='IOU_White_BG')  # IoU for the 'White_BG' class

# Register the custom IoU metrics for each class in custom_objects to allow for serialization and deserialization.
# This is useful when saving and loading the model that uses these custom metrics.
custom_objects = {
    'IOU_Not_Annotated': IOUscore0,
    'IOU_Tumor': IOUscore1,
    'IOU_Other': IOUscore2,
    'IOU_White_BG': IOUscore3
}


def calculate_intersection(class_index, pred_mask, true_mask):
    """
    Calculate the intersection part of the IoU metric for a given class index.

    Parameters:
    - class_index (int): The index of the class to calculate IoU for.
    - pred_mask (tensor): The predicted segmentation mask.
    - true_mask (tensor): The ground truth segmentation mask.

    Returns:
    - Tensor: The intersection value as part of the IoU calculation.
    """
    # Convert the specific class channel of the predicted and true masks to float32 for intersection calculation.
    pred_class_mask = tf.cast(pred_mask[..., class_index], dtype=tf.float32)
    true_class_mask = tf.cast(true_mask[..., class_index], dtype=tf.float32)

    # Calculate the intersection by finding the minimum value for each pixel location between prediction and truth.
    intersection = tf.reduce_sum(tf.math.minimum(pred_class_mask, true_class_mask))

    # Calculate the union by summing the true class mask.
    union = tf.reduce_sum(true_class_mask)

    # Add a small epsilon to avoid division by zero in case of an empty mask.
    epsilon = 1e-7
    union = tf.maximum(union, epsilon)

    # Calculate the Intersection over Union (IoU) for the class.
    iou = intersection / union

    return iou


# Below functions are designed to calculate the IoU for each individual class.
# They are wrappers around the `calculate_intersection` function, specifying the class index.
def ch_0(y_true, y_pred):
    # Calculate IoU for class index 0 ('Not_Annotated').
    return calculate_intersection(0, y_pred, y_true)


def ch_1(y_true, y_pred):
    # Calculate IoU for class index 1 ('Tumor').
    return calculate_intersection(1, y_pred, y_true)


def ch_2(y_true, y_pred):
    # Calculate IoU for class index 2 ('Other').
    return calculate_intersection(2, y_pred, y_true)


def ch_3(y_true, y_pred):
    # Calculate IoU for class index 3 ('White_BG').
    return calculate_intersection(3, y_pred, y_true)
