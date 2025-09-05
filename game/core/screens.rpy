screen RMProjectViewer():
    default Manager = RenpyManager.Manager
    default search_input = FieldInputValue(Manager, "search", default=False)
    default name_input = FieldInputValue(Manager, "project.name", default=False)
    default version_input = FieldInputValue(Manager, "project.version", default=False)

    default filter_mode = "tags"
    default mode = "lib"

    dismiss action search_input.Disable()
    key ["K_RETURN", "K_KP_ENTER"] action (search_input.Disable(), name_input.Disable(), version_input.Disable())

    timer 1 repeat True action RenpyManager.Poll()

    if persistent.rm_auto_save:
        timer persistent.rm_json_timer * 60 repeat True action RenpyManager.CacheProjects()

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
                    idle Transform("icon_gear_idle", xysize=(40, 40)) hover Transform("icon_gear_hover", xysize=(40, 40))
                    action SetLocalVariable("mode", "config") yalign 1.0

                imagebutton:
                    idle Transform("icon_save_idle", xysize=(40, 40)) hover Transform("icon_save_hover", xysize=(40, 40))
                    action RenpyManager.CacheProjects()

                imagebutton:
                    idle Transform("icon_reload_idle", xysize=(40, 40)) hover Transform("icon_reload_hover", xysize=(40, 40))
                    action RenpyManager.RefreshManager()
                
            hbox:
                align (0.5, 0.5) spacing 10
                button:
                    background RoundedImage(Solid("#ffffff22"), (300, 40)) xysize (300, 40) yalign 0.5
                    input value search_input changed Manager.refresh:
                        size 25 yalign 0.5 pixel_width 290 yoffset 2
                    action search_input.Toggle()

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
                            id "engines_vp"
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
                        
                        vbar value YScrollValue("engines_vp") xysize (5, 60) align (1.0, 0.5) xoffset -4 style "rm_vsrollbar"

                vbox:
                    spacing 10
                    text "Tags" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (425, 410), 20, trans_alpha=0.2)
                        padding (12, 8, 8, 8) ysize 410
                        vpgrid:
                            style_prefix "rm_check"
                            id "tags_vp"
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

                        vbar value YScrollValue("tags_vp") xysize (5, 370) align (1.0, 0.5) xoffset -4 style "rm_vsrollbar"
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
                        text Manager.project.name_s size 50 style "rm_title_text_bold"
                        text "[Manager.project.engine] - [Manager.project.version]" size 28 style "rm_text_bold"
                            
                        null height 3
                        text Manager.project.playtime style "rm_text" size 24
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
                        action SetLocalVariable("mode", "project_config") yalign 1.0

    elif mode == "project_config":
        frame:
            align (0.5, 0.5) xysize (1025, 1025) padding (7, 7)
            background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (1025, 1025), 20, trans_alpha=0.2)

            frame:
                background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (625, 370), 20, trans_alpha=0.2)
                padding (12, 7, 12, 7)
                xpos 385
                vbox:
                    hbox:
                        text "Name: " yalign 0.5
                        button:
                            yalign 0.5
                            input value name_input changed Manager.refresh:
                                size 27 yalign 0.5 pixel_width 380 yoffset 2
                            action name_input.Toggle()

                    hbox:
                        text "Version: " yalign 0.5
                        button:
                            yalign 0.5
                            input value version_input changed Manager.refresh:
                                size 27 yalign 0.5 pixel_width 380 yoffset 2
                            action version_input.Toggle()

                    hbox:
                        text "Executable: " yalign 0.5
                        textbutton "[Manager.project.execute_s]":
                            action RenpyManager.SelectExecutableDialog(Manager.project)
                            selected False yalign 0.5

            vbox:
                button:
                    xysize (370, 370)
                    background RoundedImage(Manager.project.thumbnail, (370, 370), radius=20)
                    action RenpyManager.SelectThumbnailDialog(Manager.project)

                spacing 20
                
                vbox:
                    spacing 10
                    text "Tags" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (440, 410), 20, trans_alpha=0.2)
                        padding (12, 8, 8, 8) xysize (440, 410)
                        vpgrid:
                            style_prefix "rm_check"
                            id "project_tags_vp"
                            draggable True mousewheel True
                            xysize (440, 395) cols 2

                            for key in Manager.tags_az:
                                button:
                                    action If(key in Manager.project.tags, ToggleDict(Manager.project.tags, key, True, False), SetDict(Manager.project.tags, key, True))
                                    text "[key!c]"
                                    xsize 205
                        
                        vbar value YScrollValue("project_tags_vp") xysize (5, 380) align (1.0, 0.5) xoffset -4 style "rm_vsrollbar"
                vbox:
                    spacing 10
                    text "Engine" xoffset 8
                    frame:
                        background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), radius=20, trans_alpha=0.2)
                        left_padding 12
                        vbox:
                            style_prefix "rm_check" box_wrap True
                            for key in [x for x in Manager.engines if x != "projects"]:
                                button:
                                    action RenpyManager.SetProjectEngine(Manager.project, key)
                                    text "[key!c]"
                                    xsize 120
                                    selected Manager.project.engine == key

            textbutton "Return" align (1.0, 1.0) text_size 45:
                text_font "fonts/Luis Georce Cafe/Louis George Cafe Bold.ttf"
                action SetLocalVariable("mode", "lib")

    elif mode == "config":
        frame:
            background Solid("#00000088")
            xysize (1920, 60)
            
            imagebutton:
                idle Transform("icon_gear_idle", xysize=(40, 40)) hover Transform("icon_gear_hover", xysize=(40, 40))
                action SetLocalVariable("mode", "lib") yalign 0.5 xoffset 10
        
        frame:
            align (0.5, 1.0) xysize (990, 990) padding (12, 7, 12, 7) yoffset -15
            background RoundedImage(Gradient(colors=("#77cbd3", "#283149", "#77cbd3", "#283149")), (990, 990), 20, trans_alpha=0.2)

            vbox:
                style_prefix "rm_check" offset (10, 10)
                
                text "Auto Cache" size 25
                null height 5
                button:
                    action ToggleField(persistent, "rm_auto_save", True, False)
                    text "Enable Auto Caching"
                    selected persistent.rm_auto_save

                if renpy.os.name == "posix":
                    null height 25

                    text "Launch Options" size 25
                    null height 5
                    button:
                        action ToggleField(persistent, "rm_execute_mode", "sh", None)
                        text "Prefer '.sh'"
                        selected persistent.rm_execute_mode == 'sh'

                    button:
                        action ToggleField(persistent, "rm_execute_mode", "py", None)
                        text "Prefer '.py'"
                        selected persistent.rm_execute_mode == 'py'

                    null height 25
                    text "Path Options" size 25
                    null height 5

                    button:
                        action ToggleField(persistent, "rm_snark_hack", "py", None)
                        text "Enable '../' Prefix"
                        selected persistent.rm_snark_hack

screen RMAbout():
    dismiss action Hide(transition=Dissolve(0.2))

    add Solid("#000000cd")
    text _("""
    Renpy Manager - v[config.version]
    
    Made by Lucy - {a=https://github.com/Luficerx}Luficerx{/a} on Github

    Renpy Manager is a simple project that handles game projects
    Mainly focused on renpy games but it tries to support different engines.

    If you encounter any bugs, Have suggestions or other stuff, please submit
    an issue on Github {a=https://github.com/Luficerx/RenpyManager}RenpyManager{/a}
    """):
        align (0.5, 0.5) size 25 text_align 0.5