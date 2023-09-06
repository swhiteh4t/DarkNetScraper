# Define a dictionary of color codes
COLORS = {
    'white': "\033[1;37m",
    'yellow': "\033[1;33m",
    'green': "\033[1;32m",
    'blue': "\033[1;34m",
    'cyan': "\033[1;36m",
    'red': "\033[1;31m",
    'magenta': "\033[1;35m",
    'black': "\033[1;30m",
    'darkwhite': "\033[0;37m",
    'darkyellow': "\033[0;33m",
    'darkgreen': "\033[0;32m",
    'darkblue': "\033[0;34m",
    'darkcyan': "\033[0;36m",
    'darkred': "\033[0;31m",
    'darkmagenta': "\033[0;35m",
    'darkblack': "\033[0;30m",
    'end': "\033[0;0m"
}

class ColoredText:
    """
    A class for displaying colored text in the terminal.

    Attributes:
        text (str): The text message to be wrapped in color.
        color_name (str): The name of the color to be applied.
    """

    def __init__(self, text, color_name):
        """Initialize a ColoredText object with text and color."""
        self.text = text
        self.color = COLORS[color_name]

    def __str__(self):
        """Return the text wrapped in the selected color."""
        return self.color + self.text + COLORS['end']

    def __add__(self, other):
        """Concatenate ColoredText objects with strings or other ColoredText objects."""
        if isinstance(other, ColoredText):
            return ColoredText(self.text + other.text, 'white')
        elif isinstance(other, str):
            return str(self) + other
        else:
            return NotImplemented

    def __radd__(self, other):
        """Right-side addition for concatenating ColoredText objects with strings."""
        if isinstance(other, str):
            return other + str(self)
        else:
            return NotImplemented
