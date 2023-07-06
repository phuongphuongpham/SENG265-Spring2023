#!/usr/bin/env python

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

def shapesList() -> list:
    """List of all Shapes"""
    circle1 = (CircleShape((50, 50, 50), (246, 234, 228, 1.0))).drawCircle()
    circle2 = (CircleShape((150, 50, 50), (249, 193, 187, 1.0))).drawCircle()
    circle3 = (CircleShape((250, 50, 50), (208, 182, 165, 1.0))).drawCircle()
    circle4 = (CircleShape((350, 50, 50), (110, 99, 93, 1.0))).drawCircle()
    circle5 = (CircleShape((50, 150, 50), (110, 99, 93, 1.0))).drawCircle()
    circle6 = (CircleShape((150, 150, 50), (208, 182, 165, 1.0))).drawCircle()
    circle7 = (CircleShape((250, 150, 50), (249, 193, 187, 1.0))).drawCircle()
    circle8 = (CircleShape((350, 150, 50), (246, 234, 228, 1.0))).drawCircle()

    rect1 = (RectangleShape((0, 200, 100, 30), (246, 217, 146, 1.0))).drawRect()
    rect2 = (RectangleShape((0, 230, 130, 30), (246, 207, 146, 1.0))).drawRect()
    rect3 = (RectangleShape((0, 260, 160, 30), (246, 196, 146, 1.0))).drawRect()
    rect4 = (RectangleShape((0, 290, 190, 30), (246, 176, 146, 1.0))).drawRect()
    rect5 = (RectangleShape((0, 320, 220, 30), (246, 161, 146, 1.0))).drawRect()
    rect6 = (RectangleShape((300, 200, 100, 30), (246, 217, 146, 1.0))).drawRect()
    rect7 = (RectangleShape((270, 230, 130, 30), (246, 207, 146, 1.0))).drawRect()
    rect8 = (RectangleShape((240, 260, 160, 30), (246, 196, 146, 1.0))).drawRect()
    rect9 = (RectangleShape((210, 290, 190, 30), (246, 176, 146, 1.0))).drawRect()
    rect10 = (RectangleShape((180, 320, 220, 30), (246, 161, 146, 1.0))).drawRect()

    resultList = [circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8,
                  rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10]
    return resultList

def main() -> None:
    """main method"""

    svg = SvgCanvas()
    svg.gen_art(shapesList(), (500, 500))
    output = HtmlDocument()
    output.writeTitle("Assignment 4 Part 1: My Art")
    output.writeBody(svg.content)

    output.writeToHTMLFile("a41.html")


if __name__ == "__main__":
    main()