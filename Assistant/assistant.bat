@echo off
REM Made by badooga. https://github.com/badooga/Python-Files
REM Used to open assistant.exe in conjunction with the Task Scheduler (or an equivalent of it).

cd %~dp0
START assistant.exe
exit