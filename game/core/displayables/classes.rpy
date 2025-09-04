init python early:
    class Gradient(renpy.Displayable):
        def __init__(self, size: tuple[int, int] = None, colors: tuple[str, str, str, str] = ("#282828", "#282828", "#0e0e0e", "#0e0e0e"), *args, **kwargs):
            """
            This creates a gradient with four colors.

            `size`: tuple[int, int] - width and height of this displayable.
            
            `colors`: tuple[str, str, str, str] - optional, this set the default color of this gradient.
            """
            super(Gradient, self).__init__(*args, **kwargs)

            self.size = size
            self.top_left, self.top_right, self.bottom_left, self.bottom_right = validate_gradient_colors(colors)

        def __eq__(self, other):
            if type(other) is Gradient:
                return all([
                    self.top_left == other.top_left,
                    self.top_right == other.top_right,
                    self.bottom_left == other.bottom_left,
                    self.bottom_right == other.bottom_right
                ])
            return False

        def render(self, w, h, st, at):
            size = (w, h)

            if self.size is not None:
                size = self.size

            rv = renpy.Render(*size)
            shader_rv = renpy.Render(*size)
            
            shader_rv.add_shader("2DVfx.simple_gradient")
            shader_rv.mesh = True
            shader_rv.fill((0.0, 0.0, 0.0, 1.0))
            
            shader_rv.add_uniform("u_bottom_right", self.bottom_right)
            shader_rv.add_uniform("u_bottom_left", self.bottom_left)
            shader_rv.add_uniform("u_top_right", self.top_right)
            shader_rv.add_uniform("u_top_left", self.top_left)

            rv.blit(shader_rv, (0, 0))

            return rv
    
    class AlphaGradientMask(renpy.Displayable):
        def __init__(self, image: str | None, direction=1, start=1.0, end=0.0, force=1, **kwargs):
            super(AlphaGradientMask, self).__init__(**kwargs)
            self.image = Transform(image)
            self.start = start
            self.end = end

            self.direction = direction
            self.force = force

        def render(self, w, h, st, at):
            
            child_rv = renpy.render(self.image, w, h, st, at)

            child_rv.add_shader("2DVfx.alpha_gradient")
            child_rv.mesh = True
            child_rv.add_uniform("u_alpha_start", self.start)
            child_rv.add_uniform("u_alpha_end", self.end)

            child_rv.add_uniform("u_direction", self.direction)
            child_rv.add_uniform("u_force", self.force)

            return child_rv

    class RoundedImage(renpy.Displayable):
        def __init__(self, image: str | None = None, size: tuple[int, int] = (None, None), radius: int | float | tuple[float] = (10, 10, 10, 10), alias: float = 1.0, **kwargs):
            """
            This creates a rounded borders around the image.

            `size`: tuple[int, int] - width and height of this displayable.
            
            `radius`: int | float | tuple[float] - how curved the border is.

            `alias`: float - anti-aliasing factor.
            """
            trans_kwargs = {}
            rest_kwargs = {}

            for (key, value) in kwargs.items():
                if key.startswith("trans_"):
                    trans_kwargs[key.removeprefix("trans_")] = value
                    continue
                rest_kwargs[key] = value

            super(RoundedImage, self).__init__(**rest_kwargs)
            self.image = Transform(image, xysize=size, **trans_kwargs)
            self.set_radius(radius)
            self.alias = alias
            self.size = size
        
        def render(self, w, h, st, at):
            size = (w, h)
            if self.size != (None, None):
                size = self.size

            rv = renpy.Render(*size)
            
            rv_child = self.image.render(w, h, st, at)
            rv.add_shader("2DVfx.round_mask")
            rv.mesh = True

            rv.add_uniform("u_radius", self.radius)
            rv.add_uniform("u_alias", self.alias)
            rv.blit(rv_child, (0, 0))
            return rv
    
        def set_radius(self, radius: int | float | tuple[float]):
            if type(radius) is int:
                self.radius = (radius, radius, radius, radius)
                
            else:
                match len(radius):
                    case 4: self.radius = radius
                    case 2: self.radius = (radius[0], radius[1], radius[0], radius[1])
                    case _ as leng:
                        raise Exception("Invalid amount of arguments: {leng}\nValid length is 2, 4.")