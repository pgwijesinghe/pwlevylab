;-----------------------------------------------------------------------------
;######################### Contents ##########################################
;-----------------------------------------------------------------------------

; KeyBindings
; Google Quick Search (Ctrl + Alt + S)
; Horizontal Scrolling (MB4 + Scroll)
; Quickly gather text to a Notepad (Alt + C)
; SearchBoxes (Google and YouTube) (Alt + G, Alt + y)
; Always on top (Win + Space)
; Hide/Unhide Desktop Icons (F12)




;--------------------------------------------------------------------------------
;######################### KeyBindings ##########################################
;--------------------------------------------------------------------------------

Capslock & h::SendInput {Blind}^{Left}
Capslock & j::SendInput {Blind}{Left} 
Capslock & k::SendInput {Blind}{Down}
Capslock & i::SendInput {Blind}{Up}
Capslock & l::SendInput {Blind}{Right}
Capslock & SC027::SendInput {Blind}^{right}
Capslock & o::SendInput {Backspace}
^!t::Run wt.exe			   
Capslock & e::
sleep 200
blockinput on
send {Blind}{LButton}{RButton}7eee{enter}
blockinput off
return

;---------------------------------------------------------------------------------------------------------
;######################### Google Quick Search (inside browser) ##########################################
;---------------------------------------------------------------------------------------------------------

^!s::
  Send ^c
  Send ^t
  Send ^v
  Send {Enter}
Return


;-----------------------------------------------------------------------------------------
;######################### Horizontal Scrolling ##########################################
;-----------------------------------------------------------------------------------------

; Default solution (for all other programs)
; XButton1 + Wheel for horizontal scrolling
XButton1 & WheelDown::WheelRight
XButton1 & WheelUp::WheelLeft

; MS Excel
#IfWinActive, ahk_exe EXCEL.EXE

; XButton1 + Wheel for horizontal scrolling (left)
~XButton1 & WheelUp::
    {
        SetScrollLockState, on
        send,{left}
        SetScrollLockState, off
    }
return

; Shift + Wheel for horizontal scrolling (right)
~XButton1 & WheelDown:: 
    {
        SetScrollLockState, on
        send,{right}
        SetScrollLockState, off
    }
return

#IfWinActive


;--------------------------------------------------------------------------------------------------------
;######################### Quickly gather text to a Notepad #############################################
;--------------------------------------------------------------------------------------------------------

; Copying text to Notepad for future reference
!c::
    OldClipboard := ClipboardAll
    Clipboard = ;clears the Clipboard
    Send, ^c
    ClipWait 0 ;pause for Clipboard data
    If ErrorLevel
    {
        MsgBox, No text selected!
    }
    
    IfWinNotExist, Untitled - Notepad
    {
        Run, Notepad
        WinWaitActive, Untitled - Notepad
    }
    
    ; Control, EditPaste used rather than ControlSend for much greater speed of execution
    
    Control, EditPaste, % Clipboard . chr(13) . chr(10) . chr(13) . chr(10) , , Untitled - Notepad
    Clipboard := OldClipboard
Return


;--------------------------------------------------------------------------------
;######################### SearchBoxes ##########################################
;--------------------------------------------------------------------------------

!g::
    InputBox, Search, Google Search, , , 400, 100
    if not ErrorLevel ; when cancel is not pressed
    {
        run C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe https://www.google.com/search?q="%Search%" 
    }
return

!y::
    InputBox, Search, YouTube Search, , , 400, 100
    if not ErrorLevel ; when cancel is not pressed
    {
        run C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe https://www.youtube.com/results?search_query="%Search%"
    }
return


;----------------------------------------------------------------------------------
;######################### Always on top ##########################################
;----------------------------------------------------------------------------------

#SPACE::  Winset, Alwaysontop, , A


;----------------------------------------------------------------------------------------------
;######################### Hide/Unhide Desktop Icons ##########################################
;----------------------------------------------------------------------------------------------

F12::
ControlGet, HWND, Hwnd,, SysListView321, ahk_class Progman
If HWND =
ControlGet, HWND, Hwnd,, SysListView321, ahk_class WorkerW
If DllCall("IsWindowVisible", UInt, HWND)
WinHide, ahk_id %HWND%
Else
WinShow, ahk_id %HWND%
Return


