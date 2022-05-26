# -*- coding:utf-8 -*-
"""
    Reversi(8x8) on PyQt5 Python3.80
    System Development A 2022/05/20

    quote :
    Window : https://www.sejuku.net/blog/75467, https://teratail.com/questions/150883
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
                      [-1, -1, -1, 1, 0, -1, -1, -1],
                      [-1, -1, -1, 0, 1, -1, -1, -1],
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
        if x < 0 or y < 0 or x > 8 or y > 8:
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
        # 8x8盤面を描画
        painter.setPen(Qt.black)  # Pen 黒色
        painter.drawLine(0, 100, 800, 100)  # 横線 MainWindow上座標(0,100)から(800,100)まで直線を引く
        painter.drawLine(0, 200, 800, 200)
        painter.drawLine(0, 300, 800, 300)
        painter.drawLine(0, 400, 800, 400)
        painter.drawLine(0, 500, 800, 500)
        painter.drawLine(0, 600, 800, 600)
        painter.drawLine(0, 700, 800, 700)

        painter.drawLine(100, 0, 100, 800)  # 縦線 MainWindow上座標(100,0)から(100,800)まで直線を引く
        painter.drawLine(200, 0, 200, 800)
        painter.drawLine(300, 0, 300, 800)
        painter.drawLine(400, 0, 400, 800)
        painter.drawLine(500, 0, 500, 800)
        painter.drawLine(600, 0, 600, 800)
        painter.drawLine(700, 0, 700, 800)

        # 盤面上にて 黒石白石を描画する
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == self.ItemB:
                    # 黒石を置く:
                    painter.setPen(Qt.black)  # Pen 黒色
                    painter.setBrush(Qt.black)  # 円を黒く塗りつぶすためのブラシ
                    painter.drawEllipse(QPointF(50 + x*100, 50 + y*100), 30, 30)  # 座標QPointF(...)中心に 短径長径30の黒い丸を描く(内部は黒で塗りつぶす)

                elif self.board[y][x] == self.ItemW:
                    # 白石を置く:
                    painter.setPen(Qt.white)  # Pen 白色
                    painter.drawEllipse(QPointF(50 + x*100, 50 + y*100), 30, 30)  # 座標QPointF(...)中心に 短径長径30の黒線で丸を描く(内部塗りつぶしなし)

    def mousePressEvent(self, event):
        '''
        マウスカーソルの位置座標とイベント取得->石を描画 イベントスロットに追加:
        :param event: QtCore.QEvent -> QtGui.QEnterEvent
        :return:
        '''
        pos = event.pos()  # QPoint():マウスカーソルの位置(受け取るwidgetでの相対位置)
        self.put(int(pos.x()/100), int(pos.y()/100))  # 石をカーソル位置に置く
        #self.judge()
        self.update()  # 画面更新
        super(Reversi, self).mousePressEvent(event)


    def boundingRect(self):
        return QRectF(0, 0, 800, 800)


class MainWindow(QGraphicsView):
    '''
    メインウィンドウ
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.reversi = Reversi()  # Reversiクラスのインスタンス生成
        scene.addItem(self.reversi)  # QGraphicsSceneにインスタンスreversiを追加
        scene.setSceneRect(0, 0, 800, 800)  # Windowのサイズ指定
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Reversi")


if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()  # メインウィンドウ インスタンス生成

    mainWindow.show()  # メインウィンドウ 表示
    sys.exit(app.exec_())  # 終了時処理



