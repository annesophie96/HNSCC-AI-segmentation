## Histo_Unet Short Abstract
This project develops an automated system for segmenting tumor tissues in H&E-stained tongue carcinoma slides, crucial in HNSCC analysis. We overcame sparse manual annotations by focusing on semantic segmentation and semi-ground truth. Utilizing Python and Groovy, our pipeline features an efficientnetb0 backbone in a Unet-based model. For this purpose 'training' and 'gif making' was used. The resulting Model can be found in 'model_T16EFF'.

# Groovy
There Exists 4 files. In qupath open the project with the slides in it. click on the automate dropdown then show script editor. import the scripts there andd use accordingly.

- 'all_tile_extractor_overlap16': Is used to to extract all tiles in the slide. If there is a region of interest (ROI) there must be a flag changed to true (it is indicated in the code). later we usse these tiles to infer the prediction back to qupath.
- 'anno_extractor': This was used for training the model. This is how we extracted the tiles alongsside mask to later training.
- 'export_ploygon_annotations': This was used the export the polygon annotatinos from qupath proj. In casee the qupath project's slides have other automated annotations, this could be used.
- 'imoprt_annotations': This couldd be used to import annotations back to qupath project.

# Inference 
This code gets the slide paths,model and qupath project path as input and predicts the tumor regions in the slide and sends the prediction as annotation it back to qupth.

# Execution Steps
The order is the following:

1. First you have to define the qupath directory in the config/.paqou.toml. just open the file and change the qupath_dir to where the qupath is installed.
2. Setup the env. You can find the needed packages in environment.yml.
3. Create a qupath project and add the slides and if there exsits ROIs 'goorvy scripts/import_annotations' could be used.
4. Export tiles using all_tile_extractor_overlap16.groovy. 
5. Run the following in the command line:

python inference_main.py --data_dir "path/to/data" --model_path "path/to/model" --qp "path/to/qupath/project.qpproj"

*Change the paths accordingly
