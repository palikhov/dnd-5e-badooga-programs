@echo off
REM Made by badooga. https://github.com/badooga/Python-Files
REM Lets you cd to a given directory given that you know the name of a file within it; only use this if the passed file's directory is in the PATH.
REM To use this, put this in a folder that has its PATH set up in environmental variables and then use "cdfile" as if it were a command in the cmd.

cd %~dp$PATH:1
