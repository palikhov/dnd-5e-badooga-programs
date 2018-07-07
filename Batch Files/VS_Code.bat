@echo off
REM Made by badooga. https://github.com/badooga/Python-Files
REM Used to open both a supplied file and its parent folder in Visual Studio Code. Requires VS Code to be in the PATH.
REM If used in the command line, the cmd will not close once this launched (if you can fix this, please make a pull request).
REM Considering that you need VS Code in the PATH anyway, just don't use this file in the CMD.
REM Instead, make this program the default editor for the appropriate file extensions using the Control Panel.
REM You can also edit the context menu's edit button via a program like Default Programs Editor (see below).
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
CLS
exit