import qupath.lib.gui.measure.ObservableMeasurementTableData
import static java.lang.Math.*

//Setting up Exports
imageName = getProjectEntry().getImageName()

String PATH = PROJECT_BASE_DIR

String directoryName = buildFilePath(PROJECT_BASE_DIR,"/csv");

File directory = new File(directoryName);
    if (! directory.exists()){
        directory.mkdir();
        // If you require it to make the entire directory path including parents,
        // use directory.mkdirs(); here instead.
    }

var path = buildFilePath(PROJECT_BASE_DIR, "/csv/MPPCalculations.csv")
var separator = ","

//Creating Files
File file = new File(path)
header = "Image name"+separator
var exists = file.exists()

//Creating Measurements
def ob = new ObservableMeasurementTableData();
def annotations = getAnnotationObjects()

 // This line creates all the measurements
ob.setImageData(getCurrentImageData(),  annotations);

double MPP_K15 = 0
double MPP_K30 = 0
double MPP_K50 = 0


double area_K15 = 0
double perimeter_K15 = 0

double area_K30 = 0
double perimeter_K30 = 0

double area_K50 = 0
double perimeter_K50 = 0

def pi = PI

annotations.each { 
    if (it.getDisplayedName().equals("model_T16_Ov16_K15")) {
        area_K15 = ob.getNumericValue(it, "Area µm^2")
        perimeter_K15 = ob.getNumericValue(it, "Perimeter µm")
    } else if (it.getDisplayedName().equals("model_T16_Ov16_K30")) {
        area_K30 = ob.getNumericValue(it, "Area µm^2")
        perimeter_K30 = ob.getNumericValue(it, "Perimeter µm")
    } else if (it.getDisplayedName().equals("model_T16_Ov16_K50")) {
        area_K50 = ob.getNumericValue(it, "Area µm^2")
        perimeter_K50 = ob.getNumericValue(it, "Perimeter µm")
    }
}






MPP_K15 = 0.5 * log((pow(perimeter_K15, 2)) / (4 * pi * area_K15))

MPP_K30 = 0.5 * log((pow(perimeter_K30, 2)) / (4 * pi * area_K30))

MPP_K50 = 0.5 * log((pow(perimeter_K50, 2)) / (4 * pi * area_K50))





//Writing Files
file.withWriterAppend { fw -> 
    if (!exists){
        header = header + "MPP_K15" + separator + "MPP_K30" + separator + "MPP_K50"
        fw.writeLine(header)
    }
    line=getProjectEntry().getImageName() + separator + MPP_K15 + separator + MPP_K30 + separator + MPP_K50
    line = line + System.getProperty("line.separator")
    fw.append(line)
}











