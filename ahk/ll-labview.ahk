#HotIf WinActive("ahk_exe LabVIEW.exe")

;---------------General Shortcuts------------->
Capslock & Space::Send "^{Space}" ;Quick Access
Capslock & e::Send "^e" ;Toggle FP/BD
Capslock & q::Send "^w" ;Quit Window


;---------------Quick Access Shortcuts------------->

Capslock & j:: ;JKI State Machine
{
Send "^{Space}"
sleep 100
Send "JKI State Machine"
sleep 100
Send "{Enter}"
return
}

Capslock & d:: ;Diagram Disable
{
Send "^{Space}" 
sleep 100
Send "dds"
sleep 100
Send "{Enter}"
return
}

Capslock & f:: ;For loop
{
Send "^{Space}" 
sleep 100
Send "fs"
sleep 100
Send "{Enter}"
return
}

#HotIf