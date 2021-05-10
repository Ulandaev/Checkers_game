from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from my_socket import My_socket
from threading import Thread
import time

import sys, time

black_pawns = [0, 1]

black_cell = [0] * 8
for i in range(8):
    black_cell[i] = [0] * 8

for i in [1, 3, 5, 7]:
    for j in [0, 2, 4, 6]:
        black_cell[i][j] = 1

for i in [0, 2, 4, 6]:
    for j in [1, 3, 5, 7]:
        black_cell[i][j] = 1

pawn_position = [0] * 8
for i in range(8):
    pawn_position[i] = [0] * 8

for i in range(8):
    for j in range(8):
        pawn_position[i][j] = False

# клетки в которых пешки изначально
for i in [0, 2, 6]:
    for j in [1, 3, 5, 7]:
        pawn_position[i][j] = True

for i in [1, 5, 7]:
    for j in [0, 2, 4, 6]:
        pawn_position[i][j] = True


class Pawn():
    color = None
    x = 0
    y = 0

    def __init__(self):
        pass

    def change_color(self, color1):
        self.color = color1


class Window(QMainWindow):
    # pawn_position = ()
    "это класс окна"

    def __init__(self, client):
        super().__init__()
        # self.step_game = step_listen
        self.client = client
        self.step_game = self.client.step_game
        self.mythread = MyThread(self.client)
        self.mythread.start()
        self.mythread.mysignal_game.connect(self.pawn_move, QtCore.Qt.QueuedConnection)
        # 1 создаем шахматное поле
        self.setWindowTitle("Checkers")
        self.setFixedSize(800, 800)
        self.board = QtWidgets.QLabel(self)
        self.board.setGeometry(QtCore.QRect(1, 2, 800, 800))
        self.board.setText("")
        self.board.setPixmap(QtGui.QPixmap("images/board.jpg"))
        self.board.setScaledContents(True)

        # Для каждой черной клетки доски создаем экземпляр класса Пешки
        self.pawn = [0] * 8
        for i in range(8):
            self.pawn[i] = [0] * 8

        for i in [1, 3, 5, 7]:
            for j in [0, 2, 4, 6]:
                self.pawn[i][j] = Pawn()

        for i in [0, 2, 4, 6]:
            for j in [1, 3, 5, 7]:
                self.pawn[i][j] = Pawn()

        # задаем цвета пешкам в начальном положении при старте игры , остальные пешки невидимы
        for j in [1, 3, 5, 7]:
            self.pawn[0][j].change_color("black")
            self.pawn[0][j].x = j
            self.pawn[0][j].y = 0

            self.pawn[1][j - 1].change_color("black")
            self.pawn[1][j - 1].x = j - 1
            self.pawn[1][j - 1].y = 1

            self.pawn[2][j].change_color("black")
            self.pawn[2][j].x = j
            self.pawn[2][j].y = 2

            self.pawn[5][j - 1].change_color("white")
            self.pawn[5][j - 1].x = j - 1
            self.pawn[5][j - 1].y = 5

            self.pawn[6][j].change_color("white")
            self.pawn[6][j].x = j
            self.pawn[6][j].y = 6

            self.pawn[7][j - 1].change_color("white")
            self.pawn[7][j - 1].x = j - 1
            self.pawn[7][j - 1].y = 7

        # создаем сами пешки, именно их изображения
        self.pawn_label = [0] * 8
        for i in range(8):
            self.pawn_label[i] = [0] * 8
        for i in range(8):
            for j in range(8):

                self.pawn_label[i][j] = QtWidgets.QLabel(self)
                self.pawn_label[i][j].setText("")
                self.pawn_label[i][j].setGeometry(
                    QtCore.QRect(40 + j * 90, 40 + i * 90, 90, 90))
                if pawn_position[i][j] == True and self.pawn[i][j].color == "white":
                    self.pawn_label[i][j].setPixmap(QtGui.QPixmap("images/pawn_white.png"))
                    self.pawn_label[i][j].setScaledContents(True)
                elif pawn_position[i][j] == True and self.pawn[i][j].color == "black":
                    self.pawn_label[i][j].setPixmap(QtGui.QPixmap("images/pawn_black.png"))
                    self.pawn_label[i][j].setScaledContents(True)
            print(self.pawn_label[3][4])
        self.cell_label = QtWidgets.QLabel(self)
        self.cell_label.setGeometry(QtCore.QRect(40, 40, 90, 90))
        self.cell_label.setObjectName("")

    def in_board(self, cell_x, cell_y):
        if cell_x >= 0 and cell_y >= 0 and cell_y <= 7 and cell_x <= 7:
            return True
        else:
            return False

    def eating_possibility(self, cell_x, cell_y, cell_x_new, cell_y_new):
        # print(pawn_position[self.cell_y_new][self.cell_x_new])
        if (abs(cell_x_new - cell_x) == 2) and (abs(cell_y_new - cell_y) == 2):
            self.cell_eatpos_x = cell_x + ((cell_x_new - cell_x) // 2)
            self.cell_eatpos_y = cell_y + ((cell_y_new - cell_y) // 2)
            # print("eat  ", self.cell_eat_y," ", self.cell_eat_x)
            if pawn_position[self.cell_eatpos_y][self.cell_eatpos_x] == True:
                if self.pawn[cell_y][cell_x].color != self.pawn[self.cell_eatpos_y][self.cell_eatpos_x].color:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # функция выделения клетки при щелчке мыши
    def pawn_highlight(self, cell_x, cell_y, bool):
        self.cell_label.move(cell_x * 90 + 40, cell_y * 90 + 40)
        self.cell_label.setObjectName("")
        if bool:
            self.cell_label.setStyleSheet('border-style: solid; border-width: 3px; border-color: rgb(239, 41, 41);')
        else:
            self.cell_label.setStyleSheet('')

    # функция передвижения изображения пешки
    def pawn_move(self, cell_x, cell_y, cell_x_new, cell_y_new, color):


        self.pawn_highlight(cell_x, cell_y, False)

        if color == "w":
            self.pawn[cell_y_new][cell_x_new].color = "white"
        if color == "b":
            self.pawn[cell_y_new][cell_x_new].color = "black"


        print("step to", cell_x, cell_y, cell_x_new, cell_y_new, color)

        if (self.clicked == True):
            self.clicked = False
        self.pawn_label[cell_y][cell_x].setPixmap(QtGui.QPixmap(""))
        if color == "w":
            self.pawn_label[cell_y_new][cell_x_new].setPixmap(QtGui.QPixmap("images/pawn_white.png"))
            self.step = 1
        elif color == "b":
            self.pawn_label[cell_y_new][cell_x_new].setPixmap(QtGui.QPixmap("images/pawn_black.png"))
            self.step = 0
        self.pawn_label[cell_y_new][cell_x_new].setScaledContents(True)
        self.animation = Qt.QPropertyAnimation(self.pawn_label[cell_y_new][cell_x_new], b"geometry")
        self.animation.setDuration(600)
        self.animation.setStartValue(Qt.QRect(cell_x * 90 + 40, cell_y * 90 + 40, 90, 90))

        self.animation.setEndValue(Qt.QRect(cell_x_new * 90 + 40, cell_y_new * 90 + 40, 90, 90))

        if self.step == self.step_game:
            if abs(cell_x - cell_x_new) == 2 :
                self.pawn_label[cell_y + int((cell_y_new - cell_y)/2)][cell_x + int((cell_x_new - cell_x)/2)].setPixmap(QtGui.QPixmap(""))
                pawn_position[cell_y + int((cell_y_new - cell_y)/2)][cell_x + int((cell_x_new - cell_x)/2)] = False
                self.pawn[cell_y + int((cell_y_new - cell_y)/2)][cell_x + int((cell_x_new - cell_x)/2)].color = None




        self.animation.start()
        pawn_position[cell_y][cell_x] = False
        pawn_position[cell_y_new][cell_x_new] = True
        self.pawn[cell_y][cell_x].color = None
        self.clicked = False
        # if (self.step == 1):
        #     self.step = 0
        # if (self.step == 0):
        #     self.step = 1
        print("now step is", self.step)


    step = 0  # первые ходят белые

    clicked = False

    def mousePressEvent(self, event):
        print(self.step_game)
        if self.step_game == 0:

            if self.clicked == False:

                self.point_press = event.pos()

                self.cell_x = (self.point_press.x() - 40) // 90
                self.cell_y = (self.point_press.y() - 40) // 90
                print("1 click", self.cell_y, self.cell_x)
                if self.in_board(self.cell_x, self.cell_y):
                    if pawn_position[self.cell_y][self.cell_x] == True:
                        if self.step == 0 and self.pawn[self.cell_y][self.cell_x].color == "white":
                            self.pawn_highlight(self.cell_x, self.cell_y, True)
                            self.clicked = True

            elif self.clicked == True:
                self.point_press = event.pos()
                self.cell_x_new = (self.point_press.x() - 40) // 90
                self.cell_y_new = (self.point_press.y() - 40) // 90

                if self.in_board(self.cell_x_new, self.cell_y_new):

                    if pawn_position[self.cell_y_new][self.cell_x_new] == False and black_cell[self.cell_y_new][
                        self.cell_x_new] == 1:
                        if self.step == 0:

                            if (self.cell_y_new == self.cell_y - 1) and (
                                    self.cell_x_new == self.cell_x - 1 or self.cell_x_new == self.cell_x + 1):
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn_highlight(self.cell_x, self.cell_y, False)
                                self.pawn_highlight(self.cell_x, self.cell_y, False)
                                #         self.pawn_move(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new, "w")
                                #         pawn_position[self.cell_y][self.cell_x] = False
                                #         pawn_position[self.cell_y_new][self.cell_x_new] = True
                                #         self.pawn[self.cell_y_new][self.cell_x_new].color = "white"
                                #         self.pawn[self.cell_y][self.cell_x].color = None
                                #         self.clicked = False
                                #         # self.step = 1

                                self.pawn_move(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new, "w")
                                pawn_position[self.cell_y][self.cell_x] = False
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn[self.cell_y_new][self.cell_x_new].color = "white"
                                self.pawn[self.cell_y][self.cell_x].color = None

                                self.client.send(
                                    f"G{self.cell_x}{self.cell_y}{self.cell_x_new}{self.cell_y_new}w".encode("utf-8"))

                            if self.eating_possibility(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new):
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn_highlight(self.cell_x, self.cell_y, False)
                                self.pawn_move(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new, "w")
                                pawn_position[self.cell_y][self.cell_x] = False
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn[self.cell_y_new][self.cell_x_new].color = "white"
                                self.pawn[self.cell_y][self.cell_x].color = None

                                self.cell_eat_x = self.cell_x + ((self.cell_x_new - self.cell_x) // 2)
                                self.cell_eat_y = self.cell_y + ((self.cell_y_new - self.cell_y) // 2)
                                pawn_position[self.cell_eat_y][self.cell_eat_x] = False
                                self.pawn[self.cell_eat_y][self.cell_eat_x].color = None
                                self.pawn_label[self.cell_eat_y][self.cell_eat_x].setPixmap(QtGui.QPixmap(""))

                                self.client.send(
                                    f"G{self.cell_x}{self.cell_y}{self.cell_x_new}{self.cell_y_new}w".encode("utf-8"))



                    else:
                        self.pawn_highlight(self.cell_x, self.cell_y, False)
                        self.clicked = False
        elif self.step_game == 1:
            if self.clicked == False:

                self.point_press = event.pos()

                self.cell_x = (self.point_press.x() - 40) // 90
                self.cell_y = (self.point_press.y() - 40) // 90
                print("1 click", self.cell_y, self.cell_x)
                if self.in_board(self.cell_x, self.cell_y):
                    if pawn_position[self.cell_y][self.cell_x] == True:
                        if self.step == 1 and self.pawn[self.cell_y][self.cell_x].color == 'black':
                            self.pawn_highlight(self.cell_x, self.cell_y, True)
                            self.clicked = True
            elif self.clicked == True:
                self.point_press = event.pos()
                self.cell_x_new = (self.point_press.x() - 40) // 90
                self.cell_y_new = (self.point_press.y() - 40) // 90

                if self.in_board(self.cell_x_new, self.cell_y_new):

                    if pawn_position[self.cell_y_new][self.cell_x_new] == False and black_cell[self.cell_y_new][
                        self.cell_x_new] == 1:

                        if self.step == 1:
                            if (self.cell_y_new == self.cell_y + 1) and (
                                    self.cell_x_new == self.cell_x - 1 or self.cell_x_new == self.cell_x + 1):
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn_highlight(self.cell_x, self.cell_y, False)
                                self.pawn_move(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new, "b")
                                pawn_position[self.cell_y][self.cell_x] = False
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn[self.cell_y_new][self.cell_x_new].color = "black"
                                self.pawn[self.cell_y][self.cell_x].color = None
                                # self.clicked = False
                                self.client.send(
                                    f"G{self.cell_x}{self.cell_y}{self.cell_x_new}{self.cell_y_new}b".encode("utf-8"))
                                self.step = 0
                            if self.eating_possibility(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new):
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn_highlight(self.cell_x, self.cell_y, False)
                                self.pawn_move(self.cell_x, self.cell_y, self.cell_x_new, self.cell_y_new, "b")
                                pawn_position[self.cell_y][self.cell_x] = False
                                pawn_position[self.cell_y_new][self.cell_x_new] = True
                                self.pawn[self.cell_y_new][self.cell_x_new].color = "black"
                                self.pawn[self.cell_y][self.cell_x].color = None

                                self.cell_eat_x = self.cell_x + ((self.cell_x_new - self.cell_x) // 2)
                                self.cell_eat_y = self.cell_y + ((self.cell_y_new - self.cell_y) // 2)
                                pawn_position[self.cell_eat_y][self.cell_eat_x] = False
                                self.pawn[self.cell_eat_y][self.cell_eat_x].color = None
                                self.pawn_label[self.cell_eat_y][self.cell_eat_x].setPixmap(QtGui.QPixmap(""))
                                # self.clicked = False
                                self.client.send(
                                    f"G{self.cell_x}{self.cell_y}{self.cell_x_new}{self.cell_y_new}b".encode("utf-8"))
                                self.step = 0

                    else:
                        self.pawn_highlight(self.cell_x, self.cell_y, False)
                        self.clicked = False


class Client(My_socket):
    mysignal = QtCore.pyqtSignal(int)
    mysignal_game = QtCore.pyqtSignal(int, int, int, int, str)

    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect(("127.0.0.1", 54312))
        listen_thread = Thread(target=self.listen_socket)
        listen_thread.start()
        listen_thread.join()
        return True

    def listen_socket(self, listened_socket=None):
        # global step
        # self.step = 0
        self.data_1 = []
        while True:
            data = self.recv(2048)
            print(data.decode("utf-8"))

            self.data_1 = list(data.decode("utf-8"))
            print(self.data_1)

            if self.data_1[1] == "R":
                self.step_game = int(self.data_1[0])
                print(self.step_game)
                break


class MyThread(QtCore.QThread):
    mysignal_game = QtCore.pyqtSignal(int, int, int, int, str)

    def __init__(self, client, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.client = client

    def run(self):
        self.data_1 = []
        while True:
            data = self.client.recv(2048)

            self.data_1 = list(data.decode("utf-8"))
            if (self.data_1[0] == "G"):
                self.mysignal_game.emit(int(self.data_1[1]), int(self.data_1[2]), int(self.data_1[3]),
                                        int(self.data_1[4]), self.data_1[5])


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkers")
        self.setFixedSize(400, 300)

        self.label = QtWidgets.QLabel(self)
        self.label.move(150, 50)
        self.label.resize(200, 50)
        self.label.setText("ШАШКИ")
        self.label.setStyleSheet("QLabel{font-size: 18pt}")

        self.icon = QtGui.QIcon("images/pawn_white.png")
        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(100, 150)
        self.btn.setText("Искать игру")
        self.btn.setIcon(self.icon)
        self.btn.setFixedWidth(200)
        self.btn.clicked.connect(self.search_game)

    def search_game(self):
        self.btn.close()
        self.label.setText("Поиск игры")
        self.client = Client()
        if self.client.set_up() == True:
            print("Start")
            self.window = Window(self.client)

            self.window.show()
            self.close()

    def show_game(self):
        self.window = Window(self.client)
        self.window.show()
        self.close()


def application():
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()