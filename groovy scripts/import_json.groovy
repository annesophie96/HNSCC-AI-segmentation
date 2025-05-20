import qupath.lib.io.GsonTools
import com.google.gson.*


// Get file path of annotations

def imageServer = getCurrentImageData().getServer()
def name = GeneralTools.getNameWithoutExtension(imageServer.getMetadata().getName())
def pathInput = buildFilePath(PROJECT_BASE_DIR, 'tiles', name)
def modelName = '_model_T16_Ov16'
def jsonFiles = ['','_K15','_K30','_K50'] //Default list: ['','_K15','_K30','_K50']

for (jsonFile in jsonFiles) {
	//def entry_path = getCurrentImageData().getServer().getPath().split('/')[0..-2]
	//entry_path=entry_path[1..-1].join('/')
	//print(entry_path)
	def json_filepath = pathInput + '/' + name + '_model_T16_Ov16'+jsonFile+'.json'
	print(json_filepath)

	// Read GeoJSN file and import annotation
	def file = new File(json_filepath)
	if (!file.exists()) {
		println "{$file} does not exist!"
		return
	}
	def gson = GsonTools.getInstance(true)
	def annotation = gson.fromJson(file.text, PathObject)
	addObjects(annotation)
}