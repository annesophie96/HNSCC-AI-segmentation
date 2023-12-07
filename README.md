## Histo_Unet
# Short Abstract
This project develops an automated system for segmenting tumor tissues in H&E-stained tongue carcinoma slides, crucial in HNSCC analysis. We overcame sparse manual annotations by focusing on semantic segmentation and semi-ground truth. Utilizing Python and Groovy, our pipeline features an efficientnetb0 backbone in a Unet-based model. For this purpose 'training' and 'gif making' was used. The resulting Model can be found in 'model_T16EFF'.

## Usage
# Groovy
There Exists 4 files. In qupath open the project with the slides in it. click on the automate dropdown then show script editor. import the scripts there andd use accordingly.

- 'all_tile_extractor_overlap16': Is used to to extract all tiles in the slide. If there is a region of interest (ROI) there must be a flag changed to true (it is indicated in the code). later we usse these tiles to infer the prediction back to qupath.
- 'anno_extractor': In case there are other 

# Inference 



Setup: 
1. First you have to define the qupath directory in the config/.paqou.toml. just open the file and change the qupath_dir. 
2. setup the env. You can find the needed packages in environment.yml.

Steps:
1. Create a qupath project and add the slides.
2. Export tiles using all_tile_extractor_overlap16.groovy.
3. In the inference code define the following paths:
  1. Define the path to the slides. data_dir = '...QupathProject/Tiles_0.9_256_176ov_all'
  2. Define the path to the qupath project. qp = '.../QupathProject.qpproj'
   
Run the code! after code is finished you would have 4 different annotations with different filtering factors. you could adjust this in the inference code if need
