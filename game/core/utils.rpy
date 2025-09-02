init -10 python:
    # Useful functions

    # Convert from hexcode to rgb tuples, "FFF" -> (1.0, 1.0, 1.0)
    def validate_gradient_colors(colors: list[str, tuple[float, float, float]]):
        """This functions takes a list of string or tuple colors and return their rgba values"""

        items = []

        if (type(colors) is not list) and (type(colors) is not tuple):
            raise TypeError(f"Invalid type passed to [colors] argument; {type(colors)} {colors}.")

        for i in colors:
            if type(i) is str:
                items.append(Color(i).rgba)

            elif type(i) is tuple or type(i) is str:
                items.append(tuple(i))

            else:
                raise TypeError(f"Invalid color argument: {type(i)} {i}")
        
        return items