#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

^q::
Gui, Destroy

Gui, add, Text,, [IFR] Chopper, Freq (Hz), Lens:
Gui, Add, Edit, vifr, Top, 1333 Hz, 100X

Gui, add, Text,, [KH] Shunt (kOhms), KH Gain:
Gui, Add, Edit, vkh, 50 kOhm, 10X

Gui, add, Text,, [SR830] (mV), (ms), (dB):
Gui, Add, Edit, vsr, 50 mV, 3 ms, 12 dB

Gui, add, Text,, [7265] (mV), (ms), (dB):
Gui, Add, Edit, v7265, 100 mV, 5 ms, 12 dB

Gui, Add, Button, gGenerate, Generate

Gui, Show

return

Generate:
GuiControlGet, ifr
GuiControlGet, kh
GuiControlGet, sr
GuiControlGet, 7265

Send, !{Esc}
Send (IFR) %ifr%; (KH) %kh%; (SR830) %sr%; (7265) %7265%
return

;1333Hz, top, -0.05 Vdc, upper beam, 260uW, 50kohom+10x(KH), 50mV+3ms+12db(SR830,x), 100mV+5ms+12dB(7265 for refl., X), plat 5K, 100x lens

