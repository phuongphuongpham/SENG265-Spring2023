#!/usr/bin/env python

import random as rd
from enum import Enum
from typing import List, NamedTuple

class HtmlDocument:
    """class HtmlDocument: A class create HTML document that has SVG content"""
    TAB: str = "   " # HTML indentation tab (default: 3 spaces)

    def __init__(self):
        self.title = ""
        self.style = ""
        self.body = ""
        self.__tabs: int = 0

    def increaseIndent(self) -> None:
        """Increases the number of tab characters used for indentation"""
        self.__tabs += 1

    def decreaseIndent(self) -> None:
        """Decreases the number of tab characters used for indentation"""
        self.__tabs -= 1

    def writeTitle(self, line: str) -> str:
        """Create string that represent Title part in HTML document"""
        title: str = "<html>\n" + "<head>\n"
        self.increaseIndent()
        title += HtmlDocument.TAB * self.__tabs
        title += "<title>" + line + "</title>\n"
        self.decreaseIndent()
        title += HtmlDocument.TAB * self.__tabs + "</head>\n"
        self.title = title
        return self.title

    def writeStyle(self, line: list) -> str:
        """Create string that represent Style part in HTML document"""
        style: str = "<style>\n"
        for l in line:
            style += l + "\n"
        style += "</style>\n"
        self.style = style
        return self.style

    def writeBody(self, line: list) -> str:
        """Create string that represent Body part in HTML document"""
        body: str = "<body>\n"
        self.increaseIndent()
        body += HtmlDocument.TAB * self.__tabs
        i: int = 0

        for l in line:
            body += l + "\n"

            if i == 0:
                self.increaseIndent()
            elif i >= len(line) - 2:
                self.decreaseIndent()

            body += HtmlDocument.TAB * self.__tabs
            i += 1

        body += "</body>\n" + "</html>"
        self.body = body
        return self.body

    def writeToHTMLFile(self, filename: str) -> None:
        """Write everything to HTML file"""
        file = open(filename, "w")
        file.write(self.title)
        file.write(self.style)
        file.write(self.body)
        file.close()


class SvgCanvas:
    """class SvgCanvas: A class create SVG content in HTML document"""
    def __init__(self):
        self.content = []

    def gen_art(self, line: list, canvas: tuple):
        """Generates SVG canvas"""
        svg: str = "<svg width=" + str(canvas[0]) + " height=" + str(canvas[1]) + ">"
        list_of_lines = [svg]

        for l in line:
            list_of_lines.append(l)

        svg = "</svg>"
        list_of_lines.append(svg)

        self.content = list_of_lines
        return self.content


class CircleShape:
    """class CircleShape: A Circle Shape representing an SVG circle element"""
    def __init__(self, cir: tuple, col: tuple) -> None:
        """Initialize a circle"""
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.rad: int = cir[2]

        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

    def drawCircle(self) -> str:
        """drawCircle(): draw Circle method
            <circle cx="{cx}" cy="{cy}" r="{rad}
                - cx: The x-axis coordinate of the center of the circle.
                - cy: The y-axis coordinate of the center of the circle.
                -  r: radius

            fill="rgb({red}, {green}, {blue})" fill-opacity="{op}</circle>
        """
        draw: str = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" '
        draw += f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        return draw

class RectangleShape:
    """class RectangleShape: A Rectangle Shape representing an SVG rectangle element"""
    def __init__(self, cir: tuple, col: tuple) -> None:
        """Initialize a rectangle"""
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.width: int = cir[2]
        self.height: int = cir[3]

        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

    def drawRect(self) -> str:
        """drawRect(): draw Rectangle method
            <rect x={self.rx} y={self.ry} width={self.width} height={self.height} />
                - rx: The x coordinate of the rect.
                - ry: The y coordinate of the rect.
        """
        draw: str = f'<rect x="{self.cx}" y="{self.cy}" width="{self.width}" height="{self.height}" '
        draw += f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        return draw

class EllipseShape:
    """class EllipseShape: A Ellipse Shape representing an SVG ellipse element"""
    def __init__(self, cir: tuple, col: tuple) -> None:
        """Initialize a ellipse"""
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.rx: int = cir[2]
        self.ry: int = cir[3]

        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

    def drawEll(self) -> str:
        """drawEll(): draw Ellipse method
        <ellipse cx={self.cx} cy={self.cy} rx={self.rx} ry={self.ry} />
            - cx: The x position of the center of the ellipse.
            - cy: The y position of the center of the ellipse.
            - rx: The x coordinate of the ell.
            - ry: The y coordinate of the ell.
        """
        draw: str = f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" '
        draw += f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        return draw

class ShapeKind(str, Enum):
    """Supported shape kinds"""
    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 2

    def __str__(self) -> str:
        return f'{self.value}'


class IntRange(NamedTuple):
    """A simple integer range with minimum and maximum values"""
    imin: int
    imax: int

    def __str__(self) -> str:
        return f'{self.imin}, {self.imax}'


class FloatRange(NamedTuple):
    """A simple float range with minimum and maximum values"""
    fmin: float
    fmax: float

    def __str__(self) -> str:
        return f'{self.fmin}, {self.fmax}'


class Extent(NamedTuple):
    """Extent definition based on width and height ranges"""
    width: IntRange
    height: IntRange

    def __str__(self) -> str:
        return f'({self.width}, {self.height})'


class Color(NamedTuple):
    """RGB color definition based on integer ranges"""
    red: IntRange
    green: IntRange
    blue: IntRange
    opacity: FloatRange

    def __str__(self) -> str:
        return f'({self.red}, {self.green}, {self.blue})'


def generateInt(r: IntRange) -> int:
    """Generates a random integer based on the range"""
    return rd.randint(r.imin, r.imax)


def generateFloat(r: FloatRange) -> float:
    """Generates a random float based on the range"""
    return rd.uniform(r.fmin, r.fmax)


class PyArtConfig:
    """class PyArtConfig: Input configuration to guide the generation of random shape"""
    def __init__(self, can: Extent = Extent(IntRange(0, 600), IntRange(0, 400)),
                 sha: List[ShapeKind] = List[ShapeKind],
                 rad: IntRange = IntRange(0, 100),
                 rxy: Extent = Extent(IntRange(10, 30), IntRange(10, 30)),
                 wah: Extent = Extent(IntRange(10, 100), IntRange(10, 100)),
                 color: Color = Color(IntRange(0, 225), IntRange(0, 225), IntRange(0, 225), FloatRange(0.0, 1.0))):
        """Initializes a configuration object with default ranges"""
        self.SHA: List[ShapeKind] = sha
        self.CAN: Extent = can
        self.RAD: IntRange = rad
        self.RXY: Extent = rxy
        self.WAH: Extent = wah
        self.COL: Color = color

    def __str__(self) -> str:
        """String representation of this configuration"""
        return f'\nUser-defined art configuration\n' \
               f'Shape types = ({", ".join(self.SHA)})\n' \
               f'CAN(CXMIN, CXMAX, CYMIN, CYMAX) = ({self.CAN})\n' \
               f'RAD(RADMIN, RADMAX) = ({self.RAD})\n' \
               f'RXY(RXMIN, RXMAX, RYMIN, RYMAX) = {self.RXY}\n' \
               f'WAH(WMIN, WMAX, HMIN, HMAX) = {self.WAH}\n' \
               f'COL(REDMIN, REDMAX, GREMIN, GREMAX, BLUMIN, BLUMAX) = {self.COL}\n' \
               f'COL(OPMIN, OPMAX) = ({self.COL.opacity.fmin:.1f}, {self.COL.opacity.fmax:1f})\n'


def randomSHA() -> int:
    """randomSHA() Generates random number for SHA"""
    shape: int = generateInt(IntRange(0, 2))
    return shape


def randomCAN() -> tuple:
    """randomCAN() Generates random number for CAN"""
    cx: int = generateInt(IntRange(0, 600))
    cy: int = generateInt(IntRange(0, 400))
    return cx, cy


def randomRAD() -> int:
    """randomRAD() Generates random number for RAD"""
    rad: int = generateInt(IntRange(0, 100))
    return rad


def randomRXY() -> tuple:
    """randomRXY() Generates random number for RXY"""
    rx: int = generateInt(IntRange(10, 30))
    ry: int = generateInt(IntRange(10, 30))
    return rx, ry


def randomWAH() -> tuple:
    """randomWAH() Generates random number for WAH"""
    width: int = generateInt(IntRange(10, 100))
    height: int = generateInt(IntRange(10, 100))
    return width, height


def randomCOL() -> tuple:
    """randomCOL() Generates random number for COL"""
    red: int = generateInt(IntRange(0, 225))
    green: int = generateInt(IntRange(0, 225))
    blue: int = generateInt(IntRange(0, 225))
    op: float = generateFloat(FloatRange(0.0, 1.0))
    return red, green, blue, op


class RandomShape:
    """class RandomShape: A class generate Random Shape from the ranges given in PyArtConfig"""
    def __init__(self):
        """Initialize the RandomShape object"""
        shape = randomSHA()
        self.sha = shape
        can = randomCAN()
        self.cx = can[0]
        self.cy = can[1]
        rad = randomRAD()
        self.rad = rad
        rxy = randomRXY()
        self.rx = rxy[0]
        self.ry = rxy[1]
        wah = randomWAH()
        self.width = wah[0]
        self.height = wah[1]
        color = randomCOL()
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        self.op = color[3]

    def __str__(self) -> str:
        """String representation of RandomShape object"""
        return f'\nRandom Shape\n' \
               f'Shape types = ({self.sha})\n' \
               f'CAN(CX, CY) = ({self.cx}, {self.cy})\n' \
               f'RAD(RADIAN) = ({self.rad})\n' \
               f'RXY(RX, RY) = ({self.rx}, {self.ry})\n' \
               f'WAH(WIDTH, HEIGHT) = ({self.width}, {self.height})\n' \
               f'COL(RED, GREEN, BLUE, OPACITY) = ({self.red}, {self.green}, {self.blue}, {self.op})\n'

    def as_svg(self) -> str:
        """as_svg(self): Create a string that represent svg element of random shapes"""
        color: tuple = (self.red, self.green, self.blue, self.op)
        if self.sha == 0:
            shape: tuple = (self.cx, self.cy, self.rad)
            svg = CircleShape(shape, color).drawCircle()

        elif self.sha == 1:
            shape: tuple = (self.cx, self.cy, self.width, self.height)
            svg = RectangleShape(shape, color).drawRect()

        else:
            shape: tuple = (self.cx, self.cy, self.rx, self.ry)
            svg = EllipseShape(shape, color).drawEll()
        return svg


def main() -> None:
    """main method"""
    svg1 = SvgCanvas()
    svg2 = SvgCanvas()
    svg3 = SvgCanvas()

    i: int = 0
    lol1 = []
    lol2 = []
    lol3 = []
    while i < 500:
        shape1 = RandomShape()
        shape2 = RandomShape()
        shape2.sha = 0
        shape3 = RandomShape()
        shape3.sha = 1
        lol1.append(shape1.as_svg())
        lol2.append(shape2.as_svg())
        lol3.append(shape3.as_svg())
        i += 1

    svg1.gen_art(lol1, (600, 400))
    svg2.gen_art(lol2, (600, 400))
    svg3.gen_art(lol3, (600, 400))
    output1 = HtmlDocument()
    output2 = HtmlDocument()
    output3 = HtmlDocument()
    output1.writeTitle("Assignment 4 Part 3: Postcard 1")
    output2.writeTitle("Assignment 4 Part 3: Postcard 2")
    output3.writeTitle("Assignment 4 Part 3: Postcard 3")
    output1.writeBody(svg1.content)
    output2.writeBody(svg2.content)
    output3.writeBody(svg3.content)

    output1.writeToHTMLFile("a431.html")
    output2.writeToHTMLFile("a432.html")
    output3.writeToHTMLFile("a433.html")


if __name__ == "__main__":
    main()

