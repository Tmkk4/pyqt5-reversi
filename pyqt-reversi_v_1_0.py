# -*- coding:utf-8 -*-
"""
    Reversi(8x8) on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
    Window : https://www.sejuku.net/blog/75467
    Widgets,Graphics :https://qiita.com/kenasman/items/73d01df973a25ae704e4
    MsgBox : https://webbibouroku.com/Blog/Article/qgis3-python-messagebox , https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
"""

import sys
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMessageBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QBrush, QColor, QPainter


class Reversi(QGraphicsItem):
    '''
    描画するアイテム : disks(黒石と白石)
    - マス目の状態 : Reversi.board[]
        - 空きマス : -1
        - 黒石(ItemB) : 0
        - 白石(ItemW) : 1
    - 現在の手番 : Reversi.turn -> 0 OR 1
    '''
    def __init__(self):
        # 初期化
        super(Reversi, self).__init__()
        self.board = [[-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1]]  # 8x8盤面状態を保持する配列
        self.ItemB = 0  # 定義 黒石 : 0
        self.ItemW = 1  # 定義 白石 : 1
        self.turn = self.ItemB  # 先手 : 0(黒石)

    def replay(self):
        # もう一度最初からプレイ
        pass

    def put(self, x, y):
        '''
        盤面上のマス目(x,y)に, 黒石か白石を置く
        :param x: 盤面上での置く位置のx座標(0~7)
        :param y: 盤面上での置く位置のy座標(0~7)
        :return: none
        '''
        if x < 0 or y < 0 or x >= 7 or y >= 7:
            # 盤面の範囲外は 石配置不可
            return

        if self.board[y][x] == -1:
            # 方向 : 行列
            # マス目 : 空状態 -> 手番の石を置いて, 黒石(0)か白石(1)へ
            self.board[y][x] = self.turn
            self.turn = 1 - self.turn  # 手番を相手の番へ

    def paint(self, painter, option, widget):
        '''
        8x8盤面の格子と黒石白石を描画する(paint()のoverridden)
        :param painter: widget上に描画を行うPen
        :param option:
        :param widget: 描画する領域
        :return:
        '''
        painter.setPen(Qt.black)  # Pen 黒色
        painter.drawLine(0, 100, 300, 100)  # (0,100)から(300,100)まで線を引く
        painter.drawLine(0, 200, 300, 200)
        painter.drawLine(100, 0, 100, 300)
        painter.drawLine(200, 0, 200, 300)


class MainWindow(QGraphicsView):
    '''
    メインウィンドウ
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.ox = Ox()  # インスタンス生成
        scene.addItem(self.ox)
        scene.setSceneRect(0, 0, 300, 300)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Reversi")


if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()  # メインウィンドウ インスタンス生成

    mainWindow.show()  # メインウィンドウ 表示
    sys.exit(app.exec_())  # 終了時処理



