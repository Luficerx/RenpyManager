# These transforms are just for showing, The way to animate shouldn't rely on these
# At least the way I programmed as is.

transform AnimatedCircle(color, rad=5.0, alias_factor=2.0):
    Null(rad*2, rad*2)
    shader "2DVfx.circle" mesh True
    u_aalias alias_factor
    u_color Color(color).rgba
    u_center (0.0, 0.0)
    u_radius (rad)

    linear 2.0 u_color Color("#ff0000").rgb
    linear 2.0 u_color Color(color).rgb
    repeat

transform AnimatedHollowCircle(color, rad, alias_factor=2.0, thickness=2.0):
    Null(rad*2, rad*2)
    shader "2DVfx.hollowcircle" mesh True
    u_alias_factor alias_factor
    u_color Color(color).rgba
    u_thickness thickness
    u_center (0.0, 0.0)
    u_radius (rad)

    easein_quad 2.0 u_thickness thickness/2
    easein_quad 2.0 u_thickness thickness
    repeat

transform AnimatedHollowArc(color, rad, alias_factor=2.0, thickness=2.0, progress=0.0, rotation=0.0):
    Null(rad*2, rad*2)
    shader "2DVfx.hollowarc" mesh True
    u_alias_factor alias_factor
    u_color Color(color).rgba
    u_thickness thickness
    u_progress progress
    u_rotation rotation
    u_center (0.0, 0.0)
    u_radius (rad)

    block:
        u_rotation rotation u_progress progress
        ease_quad 1.15 u_rotation 1.0 u_progress 0.8
        ease_quad 1.15 u_rotation 2.0 u_progress progress
        # easein_quad 1.0 u_rotation 0.0 #u_progress progress
        repeat
