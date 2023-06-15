#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Esc:: Gui Cancel

!p::
Gui, Destroy

Gui, Add, Text, x10 y10 w100 h20, Act as:
Gui, Add, Edit, x60 y10 w200 h20 vContext

Gui, Add, Tab2, x10 y40 w400 h300, Query|Compose|Coding|Task

Gui, Tab, 1
Gui, Add, Text, r1, Difference:
Gui, Add, Edit, r2 w300 vQueryDiff
Gui, Add, Text, r1, Meaning:
Gui, Add, Edit, r2 w300 vQueryMeaning
Gui, Add, Text, r1, Explain:
Gui, Add, Edit, r2 w300 vQueryExplain
Gui, Add, Button, x170 y360 w80 h30 gGeneratePromptQuery, Generate Prompt

Gui, Tab, 2
Gui, Add, ListBox, r5 vComposeType, Essay|Article|Email|Paragraph
Gui, Add, ListBox, r5 vComposeTone, Professional|Academic|Casual|Creative
Gui, Add, ListBox, r5 vComposeLength, Long|Short
Gui, Add, Checkbox, vPlagCheck, Plagiarism-free
Gui, Add, Edit, x150 y70 w250 h100 vComposeContent

Gui, Add, Button, x170 y360 w80 h30 gGeneratePromptCompose, Generate Prompt

Gui, Tab, 3
Gui, Add, Edit, x30 y90 w340 h50 vCodingTask, Test
Gui, Add, Button, x170 y360 w80 h30 gGeneratePromptCoding, Generate Prompt

Gui, Tab, 4
Gui, Add, Edit, x30 y90 w340 h50 vTaskDescription, Test
Gui, Add, Button, x170 y360 w80 h30 gGeneratePromptTask, Generate Prompt


Gui, Show
Return

GeneratePromptQuery:
GuiControlGet, Context
GuiControlGet, ComposeType
prompt := "Write a paragraph about your favorite hobby as a " . ComposeType "."
Send, !{Esc}
Send %prompt%
Return

GeneratePromptCompose:
GuiControlGet, Context
GuiControlGet, ComposeType
GuiControlGet, ComposeTone
GuiControlGet, ComposeContent
GuiControlGet, ComposeLength
GuiControlGet, PlagCheck
If PlagCheck = 0
prompt := "Act as a/an " . Context ". Write an " . ComposeType " about the following: " . ComposeContent ". The tone should be " . ComposeTone ". The length should be " . ComposeLength "."
If PlagCheck = 1
prompt := "Act as a/an " . Context ". Write an " . ComposeType " about the following: " . ComposeContent ". The tone should be " . ComposeTone ". The length should be " . ComposeLength ". It should be Plagiarism free."
Send, !{Esc}
Send %prompt%
Return

GeneratePromptCoding:
GuiControlGet, Context
GuiControlGet, ComposeType
prompt := "Write a paragraph about your favorite hobby as a " . ComposeType "."
Send, !{Esc}
Send %prompt%
Return

GeneratePromptTask:
GuiControlGet, Context
GuiControlGet, ComposeType
prompt := "Write a paragraph about your favorite hobby as a " . ComposeType "."
Send, !{Esc}
Send %prompt%
Return