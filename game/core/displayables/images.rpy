image icon_help_idle:
    alpha 0.5
    "icon_help_hover"

image icon_help_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/help_icon.png"

image icon_menu_idle:
    alpha 0.5
    "icon_menu_hover"

image icon_menu_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/menu_icon.png"

image icon_grid_idle:
    alpha 0.5
    "icon_grid_hover"

image icon_grid_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/grid_icon.png"

image icon_reload_idle:
    alpha 0.5
    "icon_reload_hover"

image icon_reload_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/reload_icon.png"

image icon_save_idle:
    alpha 0.5
    "icon_save_hover"

image icon_save_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/save_icon.png"

image icon_play_idle:
    alpha 0.5
    "icon_play_hover"

image icon_play_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/play_icon.png"

image icon_gear_idle:
    alpha 0.5
    "icon_gear_hover"

image icon_gear_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/gear_icon.png"

image icon_filter:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF") xysize (30, 30) alpha 0.3
    "images/icons/filter_icon.png"

image icon_pin_idle:
    alpha 0.5
    "icon_pin_hover"

image icon_pin_hover:
    matrixcolor ColorizeMatrix(persistent.rm_ui_color, "#FFFFFF")
    "images/icons/pin_icon.png"

image bar_stars:
    matrixcolor ColorizeMatrix("#FFFFFF", persistent.rm_ui_color)
    "images/icons/stars.png"

image thumbnail_placeholder = Fixed(Gradient(), Transform("images/logos/placeholder_logo.png", align=(0.5, 0.5), matrixcolor=ColorizeMatrix("#ACACAC", "000"), zoom=0.4))
image logo_placeholder = Transform("images/logos/placeholder_logo.png", align=(0.5, 0.5), matrixcolor=ColorizeMatrix("#ACACAC", "000"), zoom=0.5)

image renpy_thumbnail_placeholder = Fixed(Gradient(), Transform("images/logos/renpy_logo.png", align=(0.5, 0.5), zoom=0.5))
image unity_thumbnail_placeholder = Fixed(Gradient(), Transform("images/logos/unity_logo.png", align=(0.5, 0.5), zoom=0.4))
image godot_thumbnail_placeholder = Fixed(Gradient(), Transform("images/logos/godot_logo.png", align=(0.5, 0.5), zoom=0.5))

image renpy_logo_placeholder = Transform("images/logos/renpy_logo.png", align=(0.5, 0.5), zoom=0.5)
image unity_logo_placeholder = Transform("images/logos/unity_logo.png", align=(0.5, 0.5), zoom=0.5)
image godot_logo_placeholder = Transform("images/logos/godot_logo.png", align=(0.5, 0.5), zoom=0.5)