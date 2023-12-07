import qupath.lib.io.GsonTools
import com.google.gson.*


// Get file path of annotations
def imageServer = getCurrentImageData().getServer()
def name = GeneralTools.getNameWithoutExtension(imageServer.getMetadata().getName())
json_filepath = "C:/Data/Documents/Hiwis/Hamed/Annotated_ROIs/v3/" + name + ".geojson"

// Read GeoJSN file and import all annotations
def file = new File(json_filepath)
if (!file.exists()) {
    println "{$file} does not exist!"
    return
}
def gson = GsonTools.getInstance()
def features = gson.fromJson(file.text, JsonObject.class).get("features").getAsJsonArray()
def annotations = []
for (obj in features) {
    obj.addProperty("id", "PathAnnotationObject")
    annotations << gson.fromJson(obj, PathObject)
}
addObjects(annotations)