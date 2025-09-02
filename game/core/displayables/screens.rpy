screen display_gradients():
    add Solid("#181818")

    frame:
        background None align (0.5, 0.5)
        grid 2 2:
            spacing 5

            add Gradient((200, 200), ("F00", "000", "000", "F00"))
            add Gradient((200, 200), ("FFF", "000", "FFF", "000"))
            add Gradient((200, 200), ("FFF", "F00", "0F0", "00F"))
            add Gradient((200, 200), ("000", "000", "000", "00F"))
    
    textbutton "Return (x)" action Jump("start") keysym "K_x" align (0.0, 1.0) offset (10, -10) text_style "return_button_style"