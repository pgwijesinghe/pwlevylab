#Requires AutoHotkey v2.0

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
; Copy to one note (Alt + V)
; Jump to folder (Alt + J)

;--------------------------------------------------------------------------------
;######################### KeyBindings ##########################################
;--------------------------------------------------------------------------------
Capslock & q::Send "{Esc}"

;----------- Navigation ---------->
Capslock & h::Send "{Blind}^{Left}"
Capslock & j::Send "{Blind}{Left}"
Capslock & k::Send "{Blind}{Down}"
Capslock & i::Send "{Blind}{Up}"
Capslock & l::Send "{Blind}{Right}"
Capslock & SC027::Send "{Blind}^{right}"

;----------- Text Manipulation ---------->
Capslock & o::Send "{Blind}{Backspace}"
Capslock & p::Send "{Blind}^{Backspace}"
Capslock & t::Send "{Blind}{Home}"
Capslock & u::Send "{Blind}{End}"
Capslock & 9::Send "(){Left}"

;----------- Apps ---------->
^!t::Run "wt"

;----------- Functions ---------->
Capslock & w::AltTab

;---------------------------------------------------------------------------------
;######################### Double Click ##########################################
;---------------------------------------------------------------------------------
XButton2::
Capslock & LButton:: click 2

;-----------------------------------------------------------------------------------
;######################### Suspend Script ##########################################
;-----------------------------------------------------------------------------------
#SuspendExempt
F9::Suspend -1
#SuspendExempt False