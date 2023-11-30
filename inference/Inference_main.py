from tensorflow.keras.models import load_model
import cv2
from funcs import *  # Import all functions from funcs module
from metrics import *  # Import all functions from metrics module




# Path to the directory containing the image tiles
data_dir = 'D:/Hamed/Forschungsproject/Hancock 1/Tiles_0.9_256_176ov_all'

# Load the model with custom metrics and loss functions
model_T16 = load_model('./model_T16EFF',
                       custom_objects={'CategoricalCELoss': WCat, 'ch_0': ch_0, 'ch_1': ch_1,
                                       'ch_2': ch_2, 'ch_3': ch_3})

# Path to the QuPath project file
qp = 'D:/Hamed/Forschungsproject/Hancock 3/project.qpproj'

# Scaling factor for image dimensions
scaling_factor = 4.627844195912071

# Iterate over slide paths retrieved from the data directory
for slide_path in get_slide_path(data_dir):

    tiles = get_image_path(slide_path)  # Retrieve paths for image tiles
    print('Number of images =', len(tiles))

    # Get dimensions of the slide and adjust according to scaling factor
    height, width = get_dim(slide_path)
    height = int(height // scaling_factor)
    width = int(width // scaling_factor)
    print('width =', width, 'height =', height)

    # Perform prediction on images with an overlap, using the loaded model
    pred_normal16 = pred_images_overlap(tiles, batch_size=100, height=height, width=width,
                                        overlap=16, model=model_T16)

    # Calculate the modes from the predictions
    modes = cal_mode(pred_normal16, height, width)
    print('Modes Done')

    # Output the path of the current slide being processed
    print(slide_path)

    # Test and annotate the predictions in QuPath project
    test_qupath_annotation(qp, slide_path, modes, model='model_T16_Ov16')

    # Apply morphological operations at different kernel sizes to the prediction
    for i in [15, 30, 50]:
        # Define the structuring element (kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (i, i))

        # Filter the prediction for a specific class (assuming class 1 here)
        filtered = (modes == 1).astype(np.uint8)

        # Apply erosion followed by dilation (opening) and then dilation followed by erosion (closing)
        filtered = cv2.erode(filtered, kernel, iterations=1)
        filtered = cv2.dilate(filtered, kernel, iterations=1)
        filtered = cv2.dilate(filtered, kernel, iterations=1)
        filtered = cv2.erode(filtered, kernel, iterations=1)

        # Annotate the processed predictions in QuPath project with the kernel size in the model name
        test_qupath_annotation(qp, slide_path, filtered, model=f'model_T16_Ov16_K{i}')
