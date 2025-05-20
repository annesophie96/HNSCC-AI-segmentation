1. Install QuPath if you do not have it installed:
	https://github.com/qupath/qupath/releases/latest
2. Install Python 3.10 via running "01-install-python.bat".
	Note: you will have an installer window pop-up. Make sure to check the "Register to PATH variable" checkbox during installation!
	You can also manually install it from here:
		https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe (for 32-bit Windows)
		https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe (for 64-bit Windows)
3. (Optional) Register Python to your Windows Path: https://realpython.com/add-python-to-path/
	Note: This should already be registered for you if you have enabled this option in the Python installer.
4. Setup your Python virtual environment via running "02-configure-environment.bat".
	Note: If you press Y at the end of "01-install-python.bat", this will run automatically.
	Do NOT change your local repository's folder name!
		If you do so, please run "02-configure-environment.bat" again!
5. (Optional) Set your QuPath installation path in "config/.paquo.toml".
	Note: If you run "02-configure-environment.bat", this should already be configured for you automatically.
		In case you get an error message that QuPath cannot be found, please make sure to set it manually.
	Make sure to only use forward slashes (/) in your path!
	Example:
		qupath_dir = "C:/Users/YourUsername/AppData/Local/QuPath-0.5.0"
6. Make a QuPath project and make a named Annotation (ROI or Region Of Interest).
	Tip: select only parts of the image that contain tissue!
7. Export tiles from your ROI by running "all_tile_extractor_overlap16.groovy" from the Automate menu.
	Tip: register groovy script folder in your QuPath settings for easier access:
		Automate -> Shared scripts... -> Set script directory...
8. Save your QuPath project and exit QuPath.
9. Run "03-inference.bat".
	Note: If you press Y at the end of "02-configure-environment.bat", this will run automatically.
	Paste your QuPath project's path when prompted.
		Example: "C:\Users\YourUsername\Path\To\ProjectFolder"
	You can also include the project's name, e.g. if you have multiple .qpproj files in the same folder.
		Example: "C:\Users\YourUsername\Path\To\ProjectFolder\project.qpproj"
	The inference should run automatically.
	After it has completed, you can reopen your project in QuPath, and you should see the automatic segmentation annotations there.
