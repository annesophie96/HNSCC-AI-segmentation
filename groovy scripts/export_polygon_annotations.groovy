def output_dir = "C:/Data/Documents/Hamed research project/Example data from Daniel/polygon_annotations/"

// Get slide name
def imageServer = getCurrentImageData().getServer()
def name = GeneralTools.getNameWithoutExtension(imageServer.getMetadata().getName())

// Create file path
def file_path = output_dir + name + ".geojson"

// Find polygon annotations
annotations = getAnnotationObjects().findAll {
    it.getROI().RoiName == "Polygon"
}

// Export to GeoJSN file
exportObjectsToGeoJson(annotations, file_path, "FEATURE_COLLECTION")

for (ann in annotations) {
    print ann.getROI()
}