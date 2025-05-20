@echo off
setlocal enabledelayedexpansion

title Run inference

set parentdir=%~dp0

set /p projectpath=Paste the path of your QuPath project here (filename optional): 

set projectname=project.qpproj
set projectdir=a

if not "x!projectpath:.qpproj=!"=="x!projectpath!" (
	for %%a in ("%projectpath%") do set "projectdir=%%~dpa"
	for %%a in ("%projectpath%") do set "projectname=%%~nxa"
	echo !projectdir!
	echo !projectname!
) else (
	set "projectdir=!projectpath!"
	cd !projectdir!
	set "projectExt=*.qpproj"
	for %%a in (%projectExt%) do set "projectname=%%a"
	cd !parentdir!
)

if not exist .venv\Scripts\activate.bat (
	call 02-configure-environment.bat
)

set "parentdir=!parentdir:\=/!"
set "projectdir=!projectdir:\=/!"
echo !parentdir!
echo !projectdir!/!projectname!

call .venv\Scripts\activate.bat && where python && python "inference/inference_main.py" --data_dir "!projectdir!/tiles" --model_path "!parentdir!/model" --qp "!projectdir!/!projectname!"

set /p=Hit ENTER to continue...
exit 0