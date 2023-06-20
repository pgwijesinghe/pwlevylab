pre=
(
Hi,

Currently we have the following requirements for our lab. I kindly request you to complete this purchasing order. The details with regard to this order are as follows.
)

sub=
(
Please let me know if you have any questions or concerns regarding this order.

Thanks,
)

WinGet, winid
WinActivate ahk_pid %winid%
sleep 100
Send, ^c
InputBox, Item, Purchase Item, , , 400, 100
run C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe https://mail.google.com/mail/u/0/?fs=1&to=papurch@pitt.edu&tf=cm
sleep 4000
Send, LevyLab Purchase Order: %Item%
Send, {Tab}
text_send(pre)
Send, {Enter 2}
Send, ^+v
Send, {Enter 2}
text_send(sub)

text_send(text){
ClipSaved := ClipBoardAll
clipboard := ""
clipboard := text
If (!ErrorLevel)
	Send, ^v
sleep 500
clipboard := ClipSaved
}