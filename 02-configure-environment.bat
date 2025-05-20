@echo off
setlocal enabledelayedexpansion

title Environment configurator

if exist .venv\ (
	rmdir .venv /s /q
)

::if not exist .venv\Scripts\activate.bat (
	py -3.10 -m venv .venv
::)
call .venv\Scripts\activate.bat && where python && py -m pip install --upgrade pip && py -m pip --version && py -m pip install -r requirements.txt

set parentdir=%~dp0
set "parentdir=!parentdir:\=/!"
::echo !parentdir!

set AppDataDir=%LocalAppData%
cd %AppDataDir%
set str1=a
set str2=b

for /d %%d in (*.*) do (
	set str1=%%d
	if not "x!str1:QuPath=!"=="x!str1!" (
	set str2=%%d
	set "AppDataDir=!AppDataDir:\=/!"
	))
	
cd !parentdir!
set InputFile=config/default-config.txt
set OutputFile=config/.paquo.toml
set "_strFind=qupath_dir = """
set "_strInsert=qupath_dir = "!AppDataDir!/!str2!""

>"%OutputFile%" (
  for /f "usebackq delims=" %%A in ("%InputFile%") do (
    if "%%A" equ "%_strFind%" (echo %_strInsert%) else (echo %%A)
  )
)

echo Environment setup done!
set /p decide=Would you like to run inference (Y/N)^?

set /a tempvar=0

if "!decide!" equ "y" set /a tempvar=1
if "!decide!" equ "Y" set /a tempvar=1

if !tempvar! equ 1 (
	start 03-inference.bat
	exit 0
) else (
	set /p=Hit ENTER to continue...
)