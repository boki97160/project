#!/usr/bin/env python
# qml-test1.py
'''
定义一个类，并继承QtCore.QObject对象，并使用@修饰符修饰pyqtSlot
创建rootContext对象，并使用setContextProperty（string, object）注册对象，    
这样在QML中就可以调用这个函数了。

这个例子运行后，如果点击鼠标的话，会在控制台打印字符串。
'''
from PyQt5.QtQuick import QQuickView
from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyClass(QObject):
    @pyqtSlot(str)    # 输入参数为str类型
    def outputString(self, string):
        print(string)
    @pyqtSlot(list) # list可以被识别
    def outputlist(self,qmllist):
        print(qmllist)
    @pyqtSlot(QVariant) # dict不能
    def outputdict(self,qmldict):
        print(qmldict.toVariant(),type(qmldict.toVariant()))

if __name__ == '__main__':
    
    app = QGuiApplication([])
    
    path = './program/test.qml'   # 加载的QML文件
    con = MyClass()

    view = QQuickView()
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl(path))

    context = view.rootContext()
    context.setContextProperty("con", con)
    view.setFramePosition(QPoint(100,100))
    view.show()

    app.exec_()
    """self.img = QtGui.QPixmap('./src/secretkeeper_chart.png')
        self.img = self.img.scaled(self.screen.width(),self.screen.height(),QtCore.Qt.KeepAspectRatio)
        h = self.img.height()
        w = self.img.width()
        self.img = self.img.scaled(round(w*0.8),round(h*0.8))
        self.patternLabel = QtWidgets.QLabel()
        self.patternLabel.setPixmap(self.img)

        self.box=QtWidgets.QWidget(self.form)
        self.box.setGeometry(0,0,w+50,h+50)

        self.grid = QtWidgets.QGridLayout(self.box)
        self.grid.addWidget(self.patternLabel,0,0,5,1)

        self.inc = QtGui.QPixmap('./src/cdd.png')
        self.incLabel = QtWidgets.QLabel()
        self.incLabel.setPixmap(self.inc)
        self.grid.addWidget(self.incLabel,0,1)
        
        self.stscount = QtWidgets.QLabel()
        self.stscount.setText("OAO")
        self.stscount.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.stscount,1,1)


        self.dec = QtGui.QPixmap('./src/kfbf.png')
        self.decLabel = QtWidgets.QLabel()
        self.decLabel.setPixmap(self.dec)
        self.grid.addWidget(self.decLabel,2,1)


        self.rowup = QtGui.QPixmap('./src/cdd.png')
        self.rowupLabel = QtWidgets.QLabel()
        self.rowupLabel.setPixmap(self.rowup)
        self.grid.addWidget(self.rowupLabel,3,1)

        self.rowdown = QtGui.QPixmap('./src/kfbf.png')
        self.rowdownLabel = QtWidgets.QLabel()
        self.rowdownLabel.setPixmap(self.rowdown)
        self.grid.addWidget(self.rowdownLabel,4,1)
        
        self.button = QtGui.QPixmap('./src/yo.png')
        self.buttonLabel = QtWidgets.QLabel()
        self.buttonLabel.setPixmap(self.button)
        self.grid.addWidget(self.buttonLabel,5,0,2,0)

        self.form.resize(w+75,h+75)
        self.form.show()
        sys.exit(self.app.exec_())"""