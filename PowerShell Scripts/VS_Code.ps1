#Made by badooga. https://github.com/badooga/Python-Files
#Used to open both a supplied file and its parent folder in Visual Studio Code. Requires VS Code to be in the PATH.
#This file is the PowerShell equivalent of VS_Code.bat found on my GitHub (see above)
#This file is slightly slower than the batch file version, but this one will prompt you to input a parameter if you don't include it in the cmd.
#If your $env:PATH isn't set via a profile, using this file in the CMD will require you to either use an absolute filepath or to cd to this file's directory.
#You can make this program the default editor for certain file extensions using the Control Panel.
#You can also edit the context menu's edit button for a given file extension via a program like Default Programs Editor (see below).
#Default Programs Editor: http://defaultprogramseditor.com/

Param(
  [Parameter(Mandatory=$True)]
   [string]$file
)
$envpath = (Get-ChildItem Env:PATH).value.split(";",[System.StringSplitOptions]::RemoveEmptyEntries)
$pathfound = $false
foreach ($element in $envpath) {
  $fullfilename = join-path -path $element -ChildPath ("$file")
  if (test-path $fullfilename) {
    cd $element
    code . "$file"
    break
  }
  if ($envpath[-1] -eq $element) {
    cd (Split-Path $file)
    code "." "$file"
  }
}