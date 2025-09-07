style rm_text is gui_text:
    size 40 

style rm_text_bold is rm_text:
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"

style rm_title_text is rm_text:
    outlines [(2, "#000", 0, 0)]

style rm_title_text_bold is rm_text_bold:
    outlines [(2, "#000", 0, 0)]
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"

style rm_button is button

style rm_check_button is button:
    left_padding 35
    background "checker_icon_off"
    selected_background "checker_icon_on"

style rm_check_text is text:
    font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"
    size 18

style rm_vsrollbar is vscrollbar:
    idle_base_bar Transform(Solid(persistent.rm_ui_color), alpha=0.15)
    idle_thumb Transform(Solid(persistent.rm_ui_color), alpha=0.4)

    hover_base_bar Transform(Solid(persistent.rm_ui_color), alpha=0.3)
    hover_thumb Transform(Solid(persistent.rm_ui_color), alpha=0.6)
