screen RMProjectViewer():
    default Manager = RenpyManager.Manager
    default query = FieldInputValue(RenpyManager.Manager, "query", default=False)

    default filter_mode = "tags"
    default mode = "lib"

    dismiss action query.Disable()

    add rm_background

    if mode == "lib":
        frame:
            background Solid("#00000088")
            xysize (1920, 60)
            
            imagebutton:
                align (1.0, 0.5) xoffset -10
                idle Transform("icon_help_idle", xysize=(40, 40)) hover Transform("icon_help_hover", xysize=(40, 40))
                action Show("RMAbout", transition=Dissolve(0.2))

            hbox:
                yalign 0.5 xoffset 10 spacing 10

                imagebutton:
                    idle Transform("icon_reload_idle", xysize=(40, 40)) hover Transform("icon_reload_hover", xysize=(40, 40))
                    action RenpyManager.RefreshManager()

                imagebutton:
                    idle Transform("icon_save_idle", xysize=(40, 40)) hover Transform("icon_save_hover", xysize=(40, 40))
                    action RenpyManager.CacheProjects()

            hbox:
                align (0.5, 0.5) spacing 10
                button:
                    background RoundedImage(Solid("#ffffff22"), (300, 40)) xysize (300, 40) yalign 0.5
                    input value query changed Manager.refresh:
                        size 25 yalign 0.5 pixel_width 290 yoffset 2
                    action query.Toggle()

                add "icon_filter" yalign 0.5
        
        frame:
            align (0.0, 1.0) xysize (435, 1000) padding (5, 5) offset (5, -10)
            background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (435, 1000), 20, trans_alpha=0.2)
            vbox:
                spacing 25
                vbox:
                    spacing 10
                    text "Engines" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 80), 20, trans_alpha=0.2)
                        padding (12, 8, 8, 8) ysize 80
                        vpgrid:
                            style_prefix "rm_check"
                            draggable True mousewheel True
                            xysize (425, 65) cols 2

                            button:
                                action Function(Manager.toggle_all_engines)
                                text "All"
                                xsize 205
                                selected all(Manager.engines.values())

                            for key in Manager.engines:
                                button:
                                    action ToggleDict(Manager.engines, key, True, False)
                                    text "[key!c]"
                                    xsize 205
                vbox:
                    spacing 10
                    text "Tags" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 410), 20, trans_alpha=0.2)
                        padding (12, 8, 8, 8) ysize 410
                        vpgrid:
                            style_prefix "rm_check"
                            draggable True mousewheel True
                            xysize (425, 395) cols 2
                            
                            button:
                                action Function(Manager.toggle_all_tags)
                                text "All"
                                xsize 205
                                selected all(Manager.tags.values())

                            for key in Manager.tags_az:
                                button:
                                    action ToggleDict(Manager.tags, key, True, False)
                                    text "[key!c]"
                                    xsize 205
                vbox:
                    spacing 10
                    text "Rating" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 80), 20, trans_alpha=0.2)
                        xysize (425, 80)
                        add "bar_stars" align (0.5, 0.5) alpha 0.25 
                        bar:
                            left_bar "bar_stars" right_bar None xysize (181, 35) align (0.5, 0.5)
                            value FieldValue(Manager, "stars_query", 5.0, force_step=0.5)

                vbox:
                    spacing 10
                    text "Others" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 80), 20, trans_alpha=0.2)
                        xysize (425, 80) left_padding 12
                        hbox:
                            style_prefix "rm_check"
                            button:
                                action ToggleDict(Manager.others, "pinned", True, False)
                                text "By Pinned"

                            button:
                                action ToggleDict(Manager.others, "stars_query", True, False)
                                text "By Stars"

        vpgrid:
            draggable True mousewheel "horizontal"
            viewport_xsize 1025 rows 2 spacing 8 align (0.5, 1.0) yoffset -30

            scrollbars "horizontal"
            scrollbar_xysize (850, 5) scrollbar_xalign 0.5 scrollbar_yoffset 15
            scrollbar_unscrollable "hide"

            for project in Manager.projects:
                button:
                    xysize (250, 250) align (0.5, 0.5)
                    background RoundedImage(project.thumbnail, (250, 250), 20, 1)
                    if project.pinned:
                        add "icon_pin_hover" xysize (40, 40) align (1.0, 0.0) alpha 0.5 zoom 0.75

                    imagebutton:
                        idle Transform("icon_play_idle", xysize=(40, 40)) hover Transform("icon_play_hover", xysize=(40, 40))
                        action RenpyManager.Execute(project)
                        align (1.0, 1.0)
                    
                    action SetField(Manager, "project", project)

        if Manager.project:
            frame:
                align (0.5, 0.0) yoffset 100 xysize (1025, 380) padding (7, 7)
                background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (1025, 380), 20, trans_alpha=0.2)
                fixed:
                    xysize (372, 371) yalign 0.5
                    add RoundedImage(Manager.project.thumbnail, (370, 370), 20) align (0.5, 0.5)
                    add AlphaGradientMask(RoundedImage("black", (372, 371), 20), direction=4, force=0.4) align (0.5, 0.5)

                    fixed:
                        xysize (181, 35) align (0.5, 1.0) yoffset -5
                        add "bar_stars" align (0.5, 0.5) alpha 0.25
                        bar:
                            left_bar "bar_stars" right_bar None xysize (181, 35) align (0.5, 0.5)
                            value FieldValue(Manager.project, "stars", 5.0, force_step=0.5)

                frame:
                    background None xysize (628, 370) align (1.0, 0.5)
                    vbox:
                        spacing 5
                        text Manager.project.name size 50 style "rm_title_text_bold"
                        text Manager.project.engine size 28 style "rm_text_bold"
                        null height 3
                        text Manager.project.description style "rm_text" size 24

                    imagebutton:
                        idle Transform("icon_pin_idle", xysize=(30, 30)) hover Transform("icon_pin_hover", xysize=(30, 30))
                        selected_idle Transform("icon_pin_hover", xysize=(30, 30))
                        action ToggleField(Manager.project, "pinned", True, False)
                        xalign 1.0
                        
                    textbutton "Launch" align (1.0, 1.0) text_size 45:
                        text_font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"
                        action RenpyManager.Execute(Manager.project)
                    
                    imagebutton:
                        idle Transform("icon_gear_idle", xysize=(40, 40)) hover Transform("icon_gear_hover", xysize=(40, 40))
                        action SetLocalVariable("mode", "config") yalign 1.0

    elif mode == "config":
        frame:
            align (0.5, 0.5) xysize (1025, 1025) padding (7, 7)
            background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (1025, 1025), 20, trans_alpha=0.2)

            vbox:
                add RoundedImage(Manager.project.thumbnail, (370, 370), 20) yalign 0.0
                spacing 20
                hbox:
                    xoffset 10
                    text "Executable: " yalign 0.5
                    textbutton "[Manager.project.execute_s]":
                        action Show("RMChangeExecutable", project=Manager.project) 
                        selected False yalign 0.5
                
                vbox:
                    spacing 10
                    text "Tags" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 410), 20, trans_alpha=0.2)
                        padding (12, 8, 8, 8) ysize 410
                        vpgrid:
                            style_prefix "rm_check"
                            draggable True mousewheel True
                            xysize (425, 395) cols 2

                            for key in Manager.tags_az:
                                button:
                                    action If(key in Manager.project.tags, ToggleDict(Manager.project.tags, key, True, False), SetDict(Manager.project.tags, key, True))
                                    text "[key!c]"
                                    xsize 205

            textbutton "Return" align (1.0, 1.0) text_size 45:
                text_font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"
                action SetLocalVariable("mode", "lib")

screen RMChangeExecutable(project):
    add "#181818" alpha 0.7
    
    dismiss action Hide()

    fixed:
        xysize (800, 1000) align (0.5, 0.5)
        vbox:
            fixed:
                xysize (800, 50)
                add RoundedImage(Gradient(), (800, 50), (15, 15, 0, 0), 1)
                text "Select an Executable" align (0.5, 0.5)
                
            for (name, path) in RenpyManager.FetchExecutables(project):
                textbutton "[name]":
                    action (RenpyManager.SetProjectExecutable(project, name, path), Hide())
                    xysize (800, 40) xalign 0.5
                    background "#373737"
                    hover_background "#505050"

screen RMAbout():
    dismiss action Hide(transition=Dissolve(0.2))

    add Solid("#000000cd")
    text _("""
    Renpy Manager - v1.0000

    Renpy Manager is a simple project that handles game projects
    Mainly focused on renpy games but it tries to support different engines.
    """):
        align (0.5, 0.5) size 25 text_align 0.5