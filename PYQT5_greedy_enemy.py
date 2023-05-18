import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QTimer, QPointF

# Constants
CELL_SIZE = 40
NUM_ROWS = 10
NUM_COLS = 10

class PacmanItem(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, CELL_SIZE, CELL_SIZE)
        self.setBrush(QBrush(Qt.yellow))

    def move_left(self):
        if self.x() > 0:
            self.moveBy(-CELL_SIZE, 0)

    def move_right(self):
        if self.x() < (NUM_COLS - 1) * CELL_SIZE:
            self.moveBy(CELL_SIZE, 0)

    def move_up(self):
        if self.y() > 0:
            self.moveBy(0, -CELL_SIZE)

    def move_down(self):
        if self.y() < (NUM_ROWS - 1) * CELL_SIZE:
            self.moveBy(0, CELL_SIZE)


class EnemyItem(QGraphicsRectItem):
    def __init__(self, pacman, parent=None):
        super().__init__(parent)
        self.setRect(0, 0, CELL_SIZE, CELL_SIZE)
        self.setBrush(QBrush(Qt.red))
        self.pacman = pacman

        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(500)

    def move(self):
        pacman_x = self.pacman.x()
        pacman_y = self.pacman.y()

        enemy_x = self.x()
        enemy_y = self.y()

        if enemy_x < pacman_x:
            if enemy_x + CELL_SIZE <= (NUM_COLS - 1) * CELL_SIZE:
                self.moveBy(CELL_SIZE, 0)
        elif enemy_x > pacman_x:
            if enemy_x - CELL_SIZE >= 0:
                self.moveBy(-CELL_SIZE, 0)

        if enemy_y < pacman_y:
            if enemy_y + CELL_SIZE <= (NUM_ROWS - 1) * CELL_SIZE:
                self.moveBy(0, CELL_SIZE)
        elif enemy_y > pacman_y:
            if enemy_y - CELL_SIZE >= 0:
                self.moveBy(0, -CELL_SIZE)


class GameView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.pacman = PacmanItem()
        self.scene.addItem(self.pacman)

        self.enemy = EnemyItem(self.pacman)
        self.scene.addItem(self.enemy)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.pacman.move_left()
        elif key == Qt.Key_Right:
            self.pacman.move_right()
        elif key == Qt.Key_Up:
            self.pacman.move_up()
        elif key == Qt.Key_Down:
            self.pacman.move_down()

        super().keyPressEvent(event)


class PacmanGame(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.view = GameView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.view.setFixedSize(CELL_SIZE * NUM_COLS, CELL_SIZE * NUM_ROWS)
        self.view.setWindowTitle("Pacman Game")
        self.view.show()


if __name__ == "__main__":
    app = PacmanGame(sys.argv)
    sys.exit(app.exec_())
