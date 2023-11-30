import os
from natsort import natsorted
from shapely.geometry import Polygon, MultiPolygon
from shapely.affinity import affine_transform
from skimage import io, color
from skimage.transform import hough_line, hough_line_peaks
from skimage import transform
import numpy as np
import cv2

from paquo.projects import QuPathProject

def get_slide_path(data_dir):
    """
       Retrieves and sorts the paths of all files in a given directory.

       Parameters:
       - data_dir (str): The directory to search for files.

       Returns:
       - list: A sorted list of file paths within the given directory.
       """
    x = []
    for filename in natsorted(os.listdir(data_dir)):
        x.append(os.path.join(data_dir, filename))
    return x

def get_image_path(data_dir):
    """
       Retrieves and sorts the paths of all PNG files in a given directory.

       Parameters:
       - data_dir (str): The directory to search for PNG files.

       Returns:
       - list: A sorted list of PNG file paths within the given directory.
       """
    png_files = []

    for filename in natsorted(os.listdir(data_dir)):
        if filename.endswith('.png'):
            png_files.append(os.path.join(data_dir, filename))

    return png_files


def get_dim(data_dir):
    """
      Retrieves the dimensions of an image specified within a text file in the directory.

      Parameters:
      - data_dir (str): The directory containing the text file with dimension information.

      Returns:
      - tuple: A tuple containing the height and width as integers.
      """
    for filename in natsorted(os.listdir(data_dir)):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as file:
                content = file.readlines()

                # Initialize variables outside the loop
                height = None
                width = None

                for line in content:
                    if line.startswith('Height:'):
                        height = int(line.split(':')[1].strip())
                    elif line.startswith('Width:'):
                        width = int(line.split(':')[1].strip())

                return height, width


def test_qupath_annotation(qupath_project, slide_path, image, scaling_factor=4.627844195912071, model='?'):
    """
    Adds annotations to a QuPath project based on contours detected in an image.

    Parameters:
    - qupath_project (str): Path to the QuPath project file (.qpproj).
    - slide_path (str): Path to the slide image file.
    - image (array): Image array in which contours are detected.
    - scaling_factor (float): Factor to scale the annotations for the QuPath project.
    - model (str): Identifier for the model used for prediction.

    Returns:
    - None
    """

    # Open project in append-mode
    with QuPathProject(qupath_project, mode="a") as qpout:
        # Get first slide
        entry = qpout.images
        for i in range(len(entry)):
            if os.path.join(data_dir, entry[i].image_name) == slide_path + '.svs':
                print('Found a match!')
                contour_binary_mask = (image == 1).astype(np.uint8)

                # Assuming you have contours already extracted
                contours, hierarchy = cv2.findContours(contour_binary_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                # Convert the contours to a list of Shapely polygons
                # check if its a list and change the -1
                polygons = [Polygon(contour.reshape(-1, 2)[:, ::1]) for contour in contours if len(contour) >= 3]

                # Create a MultiPolygon if there is more than one contour
                if len(polygons) > 1:
                    multipolygon = MultiPolygon(polygons)
                elif len(polygons) == 1:
                    multipolygon = polygons[0]
                else:
                    print("No valid contours found.")
                    return

                # Get the bounding box of the annotation
                min_x, min_y, max_x, max_y = multipolygon.bounds

                # Calculate rotation angle (keeping it 0 for now)
                rotation_angle = 90  # Adjust the rotation angle as needed

                # Mirror on y-axis, rotate, and scale the annotation
                # Scale the annotation
                scaled_multipolygon = affine_transform(multipolygon, [scaling_factor, 0, 0, scaling_factor, 0, 0])

                # Add annotation to the QuPath project
                annotation = entry[i].hierarchy.add_annotation(roi=scaled_multipolygon,
                                                               path_class=qpout.path_classes[0])
                annotation.name = model


def count_straight_lines_probabilistic_hough(image, threshold=40, min_line_length=100, max_line_gap=10):
    """
       Counts the number of straight lines in an image using the probabilistic Hough transform.

       Parameters:
       - image (array): Image array in which lines are to be detected.
       - threshold (int): Accumulator threshold parameter for Hough transform.
       - min_line_length (int): Minimum line length to be detected.
       - max_line_gap (int): Maximum gap between lines to be considered as a single line.

       Returns:
       - int: The number of detected lines in the image.
       """
    # Read the image

    image = (image == 1).astype(np.uint8)
    # Apply GaussianBlur to reduce noise and improve Hough Transform
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply Canny edge detector
    edges = cv2.Canny(blurred_image, 0, 1)

    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Apply Probabilistic Hough Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=threshold, minLineLength=min_line_length,
                            maxLineGap=max_line_gap)

    return len(lines) if lines is not None else 0


def resize_image(image, scale_factor):
    """
       Resizes an image by a scaling factor with anti-aliasing.

       Parameters:
       - image (array): The image array to be resized.
       - scale_factor (float): The factor by which to scale the image.

       Returns:
       - array: The resized image.
       """
    resized_image = transform.resize(image, (int(image.shape[0] * scale_factor),
                                             int(image.shape[1] * scale_factor)),
                                     anti_aliasing=True)
    return resized_image


def pred_images_overlap(image_paths, batch_size=1, overlap=1, height=None, width=None, scaling_factor=4.627844195912071,
                        model=None):
    """
       Combines predicted images with overlap, placing each tile in a final large image.

       Parameters:
       - image_paths (list): List of paths to the predicted images.
       - batch_size (int): Batch size for processing images.
       - overlap (int): Number of overlapping channels in the final image.
       - height (int): Height of the final combined image.
       - width (int): Width of the final combined image.
       - scaling_factor (float): Scaling factor for image resizing.
       - model (keras.Model): Model used for predicting the image tiles.

       Returns:
       - array: The final combined image.
       """
    # Initialize the final image as an empty array with shape (final_height, final_width, 4)
    final_image = np.zeros((height, width, overlap), dtype=np.uint8)

    # Define regular expression pattern to extract tile size and position information
    pattern = r'd=(\d+\.\d+),x=(\d+),y=(\d+),w=(\d+),h=(\d+)'

    # Initialize an empty list to store predictions
    all_predictions = []

    with tqdm(total=len(image_paths)) as pbar:
        for batch_start in range(0, len(image_paths), batch_size):
            # Initialize an empty batch of tiles for the current batch
            batch_tiles = np.empty((0, 256, 256, 3), dtype=np.float32)

            # Process tiles in the current batch
            for tile_path in image_paths[batch_start:batch_start + batch_size]:
                tile = cv2.imread(tile_path)
                tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)
                tile = np.resize(tile, (256, 256, 3))
                tile = tile.astype(np.float32) / 255.0
                tile = tile.reshape(1, 256, 256, 3)
                batch_tiles = np.append(batch_tiles, tile, axis=0)

                # Update the progress bar
                pbar.update(1)

            # Make predictions for the current batch
            batch_pred = model.predict(batch_tiles, verbose=0)
            batch_pred = np.argmax(batch_pred, axis=3)
            all_predictions.extend(batch_pred)

    # Create a tqdm progress bar for the loop
    with tqdm(total=len(image_paths)) as pbar:
        i = 0
        # Loop through the tile paths in your list and place each tile in the final image
        for tile_path in image_paths:

            # Extract tile size and position information from the tile path using regex
            match = re.search(pattern, tile_path)
            if match:
                x_start = int(int(match.group(2)) // scaling_factor)
                y_start = int(int(match.group(3)) // scaling_factor)
            else:
                # Handle cases where pattern does not match (e.g., invalid filenames)
                continue

            # Place the resized tile in the final image at the specified position
            for channel in range(overlap):
                # Find the next available channel

                if final_image[y_start:y_start + 256, x_start:x_start + 256, channel].max() == 0:
                    x, y = np.shape(final_image[y_start:y_start + 256, x_start:x_start + 256, channel])
                    final_image[y_start:y_start + 256, x_start:x_start + 256, channel] = all_predictions[i][0:x, 0:y]
                    break

            # Update the progress bar
            i += 1
            pbar.update(1)

    return final_image


def mode_without_zeros(arr):
    """
       Calculates the mode of an array, excluding zeros.

       Parameters:
       - arr (array): The input array.

       Returns:
       - int: The mode of the array without considering zeros.
       """
    # Exclude zeros from the array
    arr = arr[arr != 0].astype(int)
    if arr.size == 0:
        # If there are no non-zero elements, return 0
        return 0
    else:
        # Calculate the mode of the non-zero elements
        return np.bincount(arr).argmax()


def cal_mode(pred_normal, height, width):
    """
       Calculates the mode for each pixel across channels, excluding zeros, in a predicted normal image.

       Parameters:
       - pred_normal (array): The predicted image with multiple channels.
       - height (int): The height of the image.
       - width (int): The width of the image.

       Returns:
       - array: The image with the mode calculated for each pixel.
       """
    # Calculate modes for each pixel
    modes = np.zeros((height, width), dtype=int)

    non_zero_rows = np.any(pred_normal, axis=(1, 2))
    non_zero_cols = np.any(pred_normal, axis=(0, 2))

    non_zero_row_indices = np.where(non_zero_rows)[0]
    non_zero_col_indices = np.where(non_zero_cols)[0]

    for i in tqdm(non_zero_row_indices):
        for j in non_zero_col_indices:
            pixel_values = pred_normal[i, j, :]
            modes[i, j] = mode_without_zeros(pixel_values)

    return modes
