screen color_picker():
    add Solid("#181818")

    default Canvas = ColorGradient((250, 250), outline="#464646")
    default Spectrum = SpectrumGradient(Canvas, (250, 30), direction="horizontal", outline="#000")

    default RadialCanvas = ColorGradient((125, 125), outline="#464646")
    default RadialSpectrum = SpectrumRadialGradient(RadialCanvas, 117.0, 1.5, 16.0, "#000000")

    hbox:
        align (0.5, 0.5) spacing 5
        frame:
            background "#000" xysize (264, 355)
            add Gradient((260, 351)) align (0.5, 0.5)

            add Spectrum align (0.5, 0.0) yoffset 1

            fixed:
                fit_first True align (0.5, 1.0) yoffset -1
                add Canvas.solid(250, 50)
                
                button:
                    action [Notify(f"Copied {Canvas.hexcode}"), CopyToClipboard(Canvas.hexcode)]
                    add Canvas.text
                    align (0.5, 0.5)

            add Canvas align (0.5, 0.0) yoffset 37

        frame:
            background "#000" xysize (252, 355)
            add Gradient((248, 351)) align (0.5, 0.5)
            fixed:
                fit_first True align (0.5, 0.0)
                add HollowCircle("#FFF", 119.0, 1.75, 25.0) align (0.5, 0.5)
                add RadialSpectrum align (0.5, 0.5)

                frame:
                    background Gradient((129, 129), ("#090909", "#090909", "#bdbdbd", "#bdbdbd")) xysize (129, 129) align (0.5, 0.5) padding (0, 0, 0, 0)
                    add RadialCanvas align (0.5, 0.5)

            fixed:
                fit_first True align (0.5, 1.0) yoffset -1
                add RadialCanvas.solid(238, 50)
                button:
                    action [Notify(f"Copied {RadialCanvas.hexcode}"), CopyToClipboard(RadialCanvas.hexcode)]
                    add RadialCanvas.text
                    align (0.5, 0.5)

    textbutton "Return (x)" action Jump("start") keysym "K_x" align (0.0, 1.0) offset (10, -10) text_style "return_button_style"