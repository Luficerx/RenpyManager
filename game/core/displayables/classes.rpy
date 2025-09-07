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

init python:
    import os

    class ThumbnailRect(renpy.Displayable):
        focusable = True

        def __init__(self, size: tuple[int, int], parent_size: tuple[int, int], id: str = "mask", **properties):

            self.start_xpos = properties.pop("xpos", 0)
            self.start_ypos = properties.pop("ypos", 0)

            super(ThumbnailRect, self).__init__(**properties)

            self.draggable = True
            self.w, self.h = size
            self.parent_size = parent_size

            rel_size = min(self.parent_size[0], self.parent_size[1])

            self.w = min(self.w, rel_size)
            self.h = min(self.h, rel_size)

            self.x = int(parent_size[0]//2 - self.size[0]//2)
            self.y = int(parent_size[1]//2 - self.size[1]//2)

            self.pos_set = False
            self.dragging = False

            self.zorder = 0

            self.last_x = 0
            self.last_y = 0

            self.offset_x = 0
            self.offset_y = 0

            self.id = id

        def __eq__(self, other):
            if type(other) is ThumbnailRect:
                return self.id == other.id
            return False

        def add_scale(self, fac: int):
            old_w, old_h = self.w, self.h
            parent_w, parent_h = self.parent_size

            # ensure at least 1x1
            new_w = max(150, old_w + fac)
            new_h = max(150, old_h + fac)

            # keep current position, just clamp to boundaries
            new_x = self.x
            new_y = self.y

            # clamp to boundaries
            # right boundary
            if new_x + new_w > parent_w:
                new_x = parent_w - new_w
            # left boundary (check after right in case new_w > parent_w)
            if new_x < 0:
                new_x = 0
                
            # bottom boundary
            if new_y + new_h > parent_h:
                new_y = parent_h - new_h
            # top boundary (check after bottom in case new_h > parent_h)
            if new_y < 0:
                new_y = 0

            # apply the changes
            self.w, self.h = new_w, new_h
            self.x = int(new_x)
            self.y = int(new_y)

        @property
        def size(self):
            return (max(100, int(self.w)), max(100, int(self.h)))

        @property
        def pos(self):
            return (self.x, self.y)

        def render(self, w, h, st, at, *args):
            child_rv = Null(*self.size).render(*self.size, st, at)

            cw, ch = child_rv.get_size()

            self.w = cw
            self.h = ch

            fx, fy, fw, fh = (0.0, 0.0, 1.0, 1.0)

            fx = int(absolute.compute_raw(fx, cw))
            fy = int(absolute.compute_raw(fy, ch))

            fw = int(absolute.compute_raw(fw, cw))
            fh = int(absolute.compute_raw(fh, ch))
            
            if self.dragging:
                child_rv.add_focus(self, None, fx, fy, fw, fh)

            if renpy.display.focus.get_grab() != self:
                self.last_x = self.x
                self.last_y = self.y
            
            return child_rv

        def event(self, ev, x, y, st):                
            grabbed = (renpy.display.focus.get_grab() == self)

            px = int(self.last_x + x)
            py = int(self.last_y + y)

            if self.draggable and renpy.map_event(ev, "drag_activate"):
                if (x > self.x and x < self.x+self.w) and (y > self.y and y < self.y+self.h):
                    renpy.display.focus.set_grab(self)
                    
                    self.offset_x = px - self.x
                    self.offset_y = py - self.y

                    self.dragging = True
                    grabbed = True
                    
            if renpy.map_event(ev, "drag_deactivate"):
                renpy.display.focus.set_grab(None)
                self.dragging = False

            if grabbed:
                self.x = int(max(0, min(self.parent_size[0] - self.size[0], px - self.offset_x)))
                self.y = int(max(0, min(self.parent_size[1] - self.size[1], py - self.offset_y)))

    class ThumbnailMask(renpy.Displayable):
        def __init__(self, path: str, mask_size: tuple[int, int], name: str = "thumbnail", **properties):
            super(ThumbnailMask, self).__init__(**properties)
            
            self.focus = None
            self.path = path

            self.size = renpy.render(self.image, 0, 0, 0, 0).get_size()
            self.thumb = ThumbnailRect(mask_size, self.size)

            self.thumb_path = f"images/thumbnails/{name}.png"
            self.saving = False
        
        @property
        def image(self):
            if os.name == "posix" and persistent.rm_snark_hack:
                return renpy.displayable(RenpyManager.SNARKY_PREFIX + self.path)
            return renpy.displayable(self.path)

        def save_thumbnail(self):
            rv = renpy.render(self.image, *self.size, 0, 0)

            tl, tr, bl, br = self.thumb.x, self.thumb.y, self.thumb.x+self.thumb.size[0], self.thumb.y+self.thumb.size[0]
            crop_rv = rv.subsurface((tl, tr, bl, br))

            end_rv = renpy.Render(*self.thumb.size)
            end_rv.blit(crop_rv, (0, 0))

            renpy.render_to_file(end_rv, os.path.join(config.gamedir, self.thumb_path), resize=True)

        def render(self, w, h, st, at):
            mask_rv = AlphaMask(
                        Solid("#00000070", xysize=self.size),
                        Transform(RoundedImage("black", self.thumb.size, 20), xysize=self.thumb.size, pos=self.thumb.pos), invert=True).render(*self.size, st, at)

            rv = renpy.render(self.image, w, h, st, at)
            thumb_rv = self.thumb.render(w, h, st, at)
            rv.blit(thumb_rv, self.thumb.pos)
            rv.blit(mask_rv, (0, 0))

            return rv
        
        def event(self, ev, x, y, st):
            rv = self.thumb.event(ev, x, y, st)
            if rv is not None:
                return rv
            
            elif renpy.map_event(ev, "viewport_wheelup") and self.thumb.w < self.size[0] and self.thumb.h < self.size[1]:
                self.thumb.add_scale(3)

            elif renpy.map_event(ev, "viewport_wheeldown"):
                self.thumb.add_scale(-3)
            
            renpy.redraw(self, 0.0)

        def visit(self) -> list:
            return [self.thumb]