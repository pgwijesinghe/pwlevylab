# Lang: Powershell
# Copy every nth file in a folder

# Author: Pubudu W

$step = 

$files = Get-ChildItem "D:\MyDocs"
$i = 0
Do{
$files[$i] | Copy-Item -Dest "D:\MyDocs\test"
$i = $i + $step
}
While($i -le $stop)

