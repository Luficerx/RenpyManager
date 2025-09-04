style rm_text is gui_text:
    size 40 

style rm_text_bold is rm_text:
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"

style rm_title_text is rm_text:
    outlines [(2, "#000", 0, 0)]

style rm_title_text_bold is rm_text_bold:
    outlines [(2, "#000", 0, 0)]
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"

style rm_check_button is button:
    left_padding 35
    background "checker_icon_off"
    selected_background "checker_icon_on"

style rm_check_text is text:
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"
    size 18