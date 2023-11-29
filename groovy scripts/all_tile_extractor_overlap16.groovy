import qupath.lib.images.servers.LabeledImageServer
def imageData = getCurrentImageData()

// Define output path (relative to project)
def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'Tiles_0.9_256_176ov_all', name)
mkdirs(pathOutput)

// Define output resolution
double requestedPixelSize = 0.9

// Convert to downsample
double downsample = requestedPixelSize / imageData.getServer().getPixelCalibration().getAveragedPixelSize()

print imageData.getServer().getPixelCalibration().getAveragedPixelSize()
print downsample



 Create an exporter that requests corresponding tiles from the original & labeled image servers
new TileExporter(imageData)
    .downsample(downsample)     // Define export resolution
    .imageExtension('.png')     // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
    .tileSize(256)              // Define size of each tile, in pixels
    //.labeledServer(labelServer) // Define the labeled image server to use (i.e. the one we just built)
    .annotatedTilesOnly(true)// If true, only export tiles if there is a (labeled) annotation present
    .overlap(176)                // Define overlap, in pixel units at the export resolution
    .writeTiles(pathOutput)     // Write tiles to the specified directory


def Height = imageData.getServer().getMetadata().getHeight()
def Width = imageData.getServer().getMetadata().getWidth()
//
//
if (imageData && imageData.getServer() && imageData.getServer().getMetadata()) {
    def height = imageData.getServer().getMetadata().getHeight()
    def width = imageData.getServer().getMetadata().getWidth()

    def outputFile = new File(pathOutput + "/dimensions.txt")

    // Write height and width information to the file
    outputFile.text = "Height: ${height}\nWidth: ${width}"

}
print 'Done!'