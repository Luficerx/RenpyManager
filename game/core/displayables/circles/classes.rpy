init python:
    from typing import Union as T

    class RawCircle(renpy.Displayable):
        def __init__(self, color, radius, *args, **kwargs):
            """
            Creates a raw circle displayable, don't have anti-aliasing.
            
            `color`: str or tuple[float, float, float] - hex value or a tuple with the R, G, B values.

            `radius`: int or float - the circle radius.
            """

            super(RawCircle, self).__init__(*args, **kwargs)

            self.color = validate_circle_color(color)
            self.radius = radius
            self.size = (self.radius*2, self.radius*2)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            shader_rv.add_shader("2DVfx.rawcircle")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.add_uniform("u_radius", self.radius)
            shader_rv.add_uniform("u_color", self.color)
            
            rv.blit(shader_rv, (0, 0))

            return rv

    class Circle(renpy.Displayable):
        def __init__(self, color: T[str, tuple, list], radius: T[int, float] = 5.0, aalias_factor: T[int, float] = 2.0, outline: T[str, tuple, list] = None, outline_thickness: T[float, int] = 2, *args, **kwargs):
            """
            Creates a circle displayable.
            
            `color`: str or tuple[float, float, float] - hex value or a tuple with the R, G, B values.

            `radius`: int or float - the circle radius.

            `aalias_factor`: int or float - how strong the anti-aliasing interpolation is.
            """

            super(Circle, self).__init__(*args, **kwargs)
            
            self.color = validate_circle_color(color)
            self.radius = radius
            self.aalias_factor = aalias_factor
            self.size = (self.radius*2, self.radius*2)
            
            self.outline = None
            self.outline_thickness = outline_thickness

            if outline is not None:
                self.outline = validate_circle_color(outline)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            if self.outline is not None:
                shader_rv.add_shader("2DVfx.ocircle")
                shader_rv.add_uniform("u_outline", self.outline)
                shader_rv.add_uniform("u_outline_thickness", self.outline_thickness)

            else:
                shader_rv.add_shader("2DVfx.circle")
            
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.add_uniform("u_aalias", self.aalias_factor)
            shader_rv.add_uniform("u_radius", self.radius)
            shader_rv.add_uniform("u_color", self.color)

            rv.blit(shader_rv, (0, 0))

            return rv
    
    class HollowCircle(renpy.Displayable):
        def __init__(self, color, radius, alias_factor=2.0, thickness=2.0, *args, **kwargs):
            """
            Creates a hollow circle displayable.
            
            `color`: str or tuple[float, float, float] - hex value or a tuple with the R, G, B values.

            `radius`: int or float - the circle radius.

            `alias_factor`: int or float - how strong the anti-aliasing interpolation is.

            `thickness`: int or float - how thick the borders are.
            """

            super(HollowCircle, self).__init__(*args, **kwargs)

            self.color = validate_circle_color(color)
            self.radius = radius
            self.thickness = min(radius, thickness)
            self.alias_factor = alias_factor
            self.size = (self.radius*2, self.radius*2)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            shader_rv.add_shader("2DVfx.hollowcircle")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.add_uniform("u_alias_factor", self.alias_factor)
            shader_rv.add_uniform("u_thickness", self.thickness)
            shader_rv.add_uniform("u_radius", self.radius)
            shader_rv.add_uniform("u_color", self.color)
            
            rv.blit(shader_rv, (0, 0))

            return rv
    
    class HollowArc(renpy.Displayable):
        def __init__(self, color, radius, alias_factor=2.0, thickness=2.0, progress=1.0, rotation=0.5, *args, **kwargs):
            """
            Creates a hollow circle displayable.
            
            `color`: str or tuple[float, float, float] - hex value or a tuple with the R, G, B values.

            `radius`: int or float - the circle radius.

            `alias_factor`: int or float - how strong the anti-aliasing interpolation is.

            `thickness`: int or float - how thick the borders are is.

            `progress`: float - value between 0.0 ~ 1.0 is how much filled the bar is.

            `rotation`: float - value between 0.0 ~ 1.0 where 0.0 is 0 degrees and 1.0 is 360 degrees clockwise.
            """

            super(HollowArc, self).__init__(*args, **kwargs)

            self.color = validate_circle_color(color)
            self.radius = radius
            self.thickness = min(radius, thickness)
            self.alias_factor = alias_factor
            self.progress = progress
            self.rotation = rotation
            self.size = (self.radius*2, self.radius*2)

        def render(self, w, h, st, at):
            rv = renpy.Render(*self.size)
            shader_rv = renpy.Render(*self.size)
            
            shader_rv.add_shader("2DVfx.hollowarc")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            shader_rv.add_uniform("u_alias_factor", self.alias_factor)
            shader_rv.add_uniform("u_thickness", self.thickness)
            shader_rv.add_uniform("u_rotation", self.rotation)
            shader_rv.add_uniform("u_progress", self.progress)
            shader_rv.add_uniform("u_radius", self.radius)
            shader_rv.add_uniform("u_color", self.color)
            
            rv.blit(shader_rv, (0, 0))

            return rv