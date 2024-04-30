import sys
from math import sqrt, degrees, acos
from random import randint

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor
from PyQt5.QtCore import Qt, QFile, QTextStream, QPointF, QLineF


class Matrix:
    def __init__(self):
        self.data = []

    def load_from_file(self, file_path):
        file = QFile(file_path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            return False

        stream = QTextStream(file)
        self.data.clear()
        while not stream.atEnd():
            line = stream.readLine()
            row = list(map(int, line.strip().split(' ')))
            self.data.append(row)

        file.close()
        return True

    def is_valid(self):
        if not self.data:
            return False
        n = len(self.data)
        for row in self.data:
            if len(row) != n:
                return False
            for val in row:
                if val != 0 and val != 1:
                    return False
        return True


class Graph:
    def __init__(self, matrix):
        self.matrix = matrix


class GraphDrawer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.destination = QPointF(50, 50)
        self.begin = QPointF(0, 0)

    def draw_graph(self, graph_matrix):
        self.graph_matrix = graph_matrix
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))

        if not hasattr(self, 'graph_matrix'):
            return

        n = len(self.graph_matrix.data)
        pen = QPen()

        pen.setWidth(2)
        painter.setPen(pen)

        for i in range(n):
            for j in range(n):
                if self.graph_matrix.data[i][j] == 1:
                    if i % 3 == 1:
                        x_1 = 50 + i // 3 * 150 + 150
                        y_1 = 50 + i // 3 * 150

                    elif i % 3 == 2:
                        x_1 = 50 + i // 3 * 150
                        y_1 = 50 + i // 3 * 150 + 150

                    else:
                        x_1 = 50 + i // 3 * 150
                        y_1 = 50 + i // 3 * 150

                    if j % 3 == 1:
                        x_2 = 50 + j // 3 * 150 + 150
                        y_2 = 50 + j // 3 * 150

                    elif j % 3 == 2:
                        x_2 = 50 + j // 3 * 150
                        y_2 = 50 + j // 3 * 150 + 150

                    else:
                        x_2 = 50 + j // 3 * 150
                        y_2 = 50 + j // 3 * 150
                    dx = 0
                    dy = 0
                    start_point = QPointF(x_1, y_1)
                    end_point = QPointF(x_2, y_2)
                    if start_point.x() > end_point.x():
                        dx = - 20
                    elif start_point.x() < end_point.x():
                        dx = 20
                    if start_point.y() > end_point.y():
                        dy = -20
                    elif start_point.y() < end_point.y():
                        dy = 20
                    self.begin = start_point
                    self.destination = QPointF(end_point.x() - dx, end_point.y() - dy)
                    line = QLineF(start_point, end_point)
                    painter.drawLine(line)
                    self.draw_arrow(painter, line)
                    painter.translate(0, 0)
        pen.setWidth(10)
        pen.setColor(Qt.red)
        for i in range(n):
            # pen.setColor(QColor(*[randint(0, 255) for i in range(3)]))
            painter.setPen(pen)
            if i % 3 == 1:
                x = 50 + i // 3 * 150 + 150
                y = 50 + i // 3 * 150
            elif i % 3 == 2:
                x = 50 + i // 3 * 150
                y = 50 + i // 3 * 150 + 150
            else:
                x = 50 + i // 3 * 150
                y = 50 + i // 3 * 150
            painter.drawPoint(x, y)
            painter.drawText(x + 25, y + 25, str(i + 1))

    def draw_arrow(self, painter, line):
        painter.save()

        l = 30
        x_right = QPointF(self.destination + QPointF(15, 0))

        right_triangle = QPainterPath()
        right_triangle.lineTo(-0.6 * sqrt(3) * l, 0.4 * l)
        right_triangle.lineTo(-0.6 * sqrt(3) * l, -0.4 * l)
        right_triangle.closeSubpath()
        right_triangle.translate(x_right)

        painter.setBrush(QColor("blue"))
        painter.translate(self.destination)

        x1, y1 = self.begin.x(), self.begin.y()
        x2, y2 = self.destination.x(), self.destination.y()
        a = y2 - y1
        c = x2 - x1
        b = sqrt(a ** 2 + c ** 2)

        angle = 0
        if a == 0 and b == c:
            angle = 0
        elif c == 0 and -a == b:
            angle = 90
        elif a == 0 and b == -c:
            angle = 180
        elif c == 0 and a == b:
            angle = 270
        elif a < 0 and b > 0:
            angle = degrees(acos((b * b + c * c - a * a) / (2.0 * b * c)))
        else:
            angle = 360 - degrees(acos((b * b + c * c - a * a) / (2.0 * b * c)))

        painter.rotate(-angle)
        painter.translate(-self.destination)
        painter.drawPath(right_triangle)
        painter.restore()
        #painter.rotate(angle)
        # painter.translate(self.destination)
        #painter.translate(0, 0)


class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.matrix = Matrix()
        self.graph_drawer = GraphDrawer()
        self.setCentralWidget(self.graph_drawer)
        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        load_action = file_menu.addAction('Load Graph')
        load_action.triggered.connect(self.load_graph)

    def load_graph(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Graph File', '', 'Text Files (*.txt)')
        if file_path:
            if self.matrix.load_from_file(file_path) and self.matrix.is_valid():
                self.graph_drawer.draw_graph(self.matrix)
            else:
                print("Error reading or invalid graph data")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceWindow()
    window.setGeometry(100, 100, 500, 500)
    window.setWindowTitle('Graph Visualizer')
    window.show()
    sys.exit(app.exec_())

