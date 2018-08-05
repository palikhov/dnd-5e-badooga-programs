@echo off
REM Made by badooga. https://github.com/badooga/Python-Files
REM Use to automate the compiling of py files into exe files with no useless files or directories left over.
REM As seen below, the use of this program requires pyinstaller to be installed on your computer.
REM You can use this in the cmd by passing the py to be compiled as an argument (with the appropriate filepath, unless the PATH will take care of that.)
REM You can also use a program like Default Programs Editor (see below) to add this batch file to the .py extension's context menu.
REM Default Programs Editor: http://defaultprogramseditor.com/

if ["%~dp$PATH:1"] == [] (
    cd "%~dp1"
) else (
    cd "%~dp$PATH:1"
)
pyinstaller --distpath "Compiled Applications" --workpath .\exe_build_temp -F %1
if NOT ["%errorlevel%"]==["0"] (
    echo "Error: A file called '%1' was not found."
    pause
    exit /b %errorlevel%
)
set str=%1
set str2=%1
set str=%str:.py=.spec%
set str2=%str2:.json=.spec%
del %str%
del %str2%
rmdir /S /Q exe_build_temp