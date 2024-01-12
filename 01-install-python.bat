@echo off
setlocal enabledelayedexpansion

title Python auto-installer

echo This tool will install Python 3.10 on your computer.
echo It will also try to register the Python executable to your machine's Path variable. This way, Python commands should be executable automatically.
echo If the environment activator or inference batch script do not work, please register the Path manually.
echo For more information, please see here: https://realpython.com/add-python-to-path/

winget install -e -i --id Python.Python.3.10 --source=winget --scope=machine --force

set /a tempvar=0

set /p decide=Would you like to run the environment initialization (Y/N)^?

if "!decide!" equ "y" set /a tempvar=1
if "!decide!" equ "Y" set /a tempvar=1


if !tempvar! equ 1 (
	start 02-configure-environment.bat
	exit 0
) else (
	set /p=Hit ENTER to continue...
)