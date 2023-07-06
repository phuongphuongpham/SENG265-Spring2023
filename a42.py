#!/usr/bin/env python

import random as rd
from enum import Enum
from typing import List, NamedTuple

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
    def __init__(self, can: Extent = Extent(IntRange(0, 500), IntRange(0, 300)),
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
    cx: int = generateInt(IntRange(0, 500))
    cy: int = generateInt(IntRange(0, 300))
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
        """as_svg(self) Create a string that represent svg element of random shapes"""
        if self.sha == 0:
            svg = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" ' \
                  f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity={self.op}></circle>'
        elif self.sha == 1:
            svg = f'<rect x="{self.rx}" y="{self.ry}" width="{self.width}" height="{self.height}" '\
                  f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        else:
            svg = f'<ellipse cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" '\
                  f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        return svg

    def as_Part2_line(self, counter: int) -> str:
        """as_Part2_line(self, counter: int) Generates the string that represent a row in a HTML table"""
        tab: str = "   "
        row: str = ""
        if counter == -1:
            row = "<tr>\n" + 3 * tab + "<th>CNT</th>\n"
            row += 3 * tab + "<th>SHA</th>\n"
            row += 3 * tab + "<th>X</th>\n"
            row += 3 * tab + "<th>Y</th>\n"
            row += 3 * tab + "<th>RAD</th>\n"
            row += 3 * tab + "<th>RX</th>\n"
            row += 3 * tab + "<th>RY</th>\n"
            row += 3 * tab + "<th>W</th>\n"
            row += 3 * tab + "<th>H</th>\n"
            row += 3 * tab + "<th>R</th>\n"
            row += 3 * tab + "<th>G</th>\n"
            row += 3 * tab + "<th>B</th>\n"
            row += 3 * tab + "<th>OP</th>\n"
            row += 2 * tab + "</tr>"

        else:
            row = f'<tr>\n{3 * tab}<th>{counter}</th>\n' \
                  f'{3 * tab}<th>{self.sha}</th>\n' \
                  f'{3 * tab}<th>{self.cx}</th>\n' \
                  f'{3 * tab}<th>{self.cy}</th>\n' \
                  f'{3 * tab}<th>{self.rad}</th>\n' \
                  f'{3 * tab}<th>{self.rx}</th>\n' \
                  f'{3 * tab}<th>{self.ry}</th>\n' \
                  f'{3 * tab}<th>{self.width}</th>\n' \
                  f'{3 * tab}<th>{self.height}</th>\n' \
                  f'{3 * tab}<th>{self.red}</th>\n' \
                  f'{3 * tab}<th>{self.green}</th>\n' \
                  f'{3 * tab}<th>{self.blue}</th>\n' \
                  f'{3 * tab}<th>{self.op:.1f}</th>\n' \
                  f'{2 * tab}</tr>'

        return row

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


def main() -> None:
    """main method"""
    # Style
    style = ["th {\n   text-align: right;\n   width=18}"]

    # Body
    i = -1
    lol = ["<table width=550>"]
    while i < 10:
        shape = RandomShape()
        table = shape.as_Part2_line(i)
        lol.append(table)
        i += 1
    lol.append("</table>")

    # Write to output
    output = HtmlDocument()
    output.writeTitle("Assignment 4 Part 2: Random Numbers")
    output.writeBody(lol)
    output.writeStyle(style)
    output.writeToHTMLFile("a42.html")


if __name__ == "__main__":
    main()