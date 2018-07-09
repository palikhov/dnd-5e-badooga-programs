@echo off
REM Made by badooga. https://github.com/badooga/Python-Files
REM Used to open both a supplied file and its parent folder in Visual Studio Code. Requires VS Code to be in the PATH.
REM You can make this program the default editor for certain file extensions using the Control Panel.
REM You can also edit the context menu's edit button for a given file extension via a program like Default Programs Editor (see below).
REM Default Programs Editor: http://defaultprogramseditor.com/

if [%1] == [] (
    echo "Error: File parameter not found."
    pause
    exit
)

if ["%~dp$PATH:1"] == [""] (
    cd %~dp1
) else (
    cd %~dp$PATH:1
)
start /MAX "" code . "%~nx1"
exit