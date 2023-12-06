from tensorflow.keras.models import load_model
import argparse
import cv2

from segmentation_models.losses import *

from funcs import (
    get_slide_path,
    get_image_path,
    get_dim,
    test_qupath_annotation,
    pred_images_overlap,
    cal_mode
)

from metrics import (
    calculate_intersection,
    ch_0,
    ch_1,
    ch_2,
    ch_3
)


def main(data_dir, model_path, qp):
    WCat = CategoricalCELoss(class_weights=[0, 1, 1, 1])

    # Load the model with custom metrics and loss functions
    model_T16 = load_model(model_path,
                           custom_objects={'CategoricalCELoss': WCat, 'ch_0': ch_0, 'ch_1': ch_1,
                                           'ch_2': ch_2, 'ch_3': ch_3})

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
        print(f'predict tiles in {slide_path}')
        pred_normal16 = pred_images_overlap(tiles, batch_size=100, height=height, width=width,
                                            overlap=16, model=model_T16)

        # Calculate the modes from the predictions
        print('Calculating the mode')
        modes = cal_mode(pred_normal16, height, width)

        # Test and annotate the predictions in QuPath project
        print('importing raw prediction to qupath')
        test_qupath_annotation(data_dir, qp, slide_path, modes, model='model_T16_Ov16')

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
            print(f'importing filtered prediction K={i} to qupath')
            test_qupath_annotation(data_dir, qp, slide_path, filtered, model=f'model_T16_Ov16_K{i}')
        break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process image tiles and perform predictions and infer to qupath.")
    parser.add_argument("--data_dir", required=True, help="Path to the slides")
    parser.add_argument("--model_path", required=True, help="Path to the trained model file")
    parser.add_argument("--qp", required=True, help="Path to the QuPath project file")
    args = parser.parse_args()

    main(args.data_dir, args.model_path, args.qp)
