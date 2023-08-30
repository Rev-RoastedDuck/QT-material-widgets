from PySide6.QtCore import QRect, QSize, Qt, QTimer, QRegularExpression
from PySide6.QtGui import QBrush, QColor, QCursor, QFont, QPainter, QPainterPath, QIcon
from PySide6.QtWidgets import QApplication, QFrame, QPushButton,QWidget

import icon
from Qss_GetProperty import get_property,transfer_type

class RWavyButton(QFrame):
    def __init__(self,parent=None):
        super(RWavyButton, self).__init__(parent)
        self.setObjectName("RWavyButton")
        self.componentInit()

    def componentInit(self):
        '''
        初始化需要的组件
        :return:
        '''
        self.pushButton = QPushButton(self)

    def uiConfig(self):
        '''
        设置组件样式
        :return:
        '''
        self.setFixedSize(self.width(),self.height())
        self.pushButton.setFixedSize(self.width(),self.height())
        self.pushButton.setStyleSheet(u"QPushButton{{"
                                      "	border:none;"
                                      "	background-color:rgba(255,255,255,0);"
                                      " border-radius:{}px;"
                                      "	color: {};"
                                      "}}".format(self.border_radius,self.font_color)
                                      )

    def getStyleSheetConfig(self):
        '''
        提取样式
        :return:
        '''
        RWavyButton_property:dict = get_property(self)["#RWavyButton"]
        
        self.border_radius = transfer_type(RWavyButton_property["border-radius"],"pixel")
        self.full_color = transfer_type(RWavyButton_property["R-full-color"],"color")
        self.font_color = RWavyButton_property["R-font-color"]

    def animationConfig(self):
        self.center = None                                         # 鼠标点击坐标
        self.radiusVar = 2                                         # 半径变化值
        self.radius = 0                                            # 起始半径
        self.max_radius = (self.width()**2+self.height()**2)**0.5  # 最大半径
        self.msec = 10                                             # 定时时间

        self.is_leave: bool = False
        self.timer = QTimer(self)
        self.timer.setInterval(self.msec)
        self.timer.timeout.connect(self.incRadius)

    def incRadius(self):
        self.radius += self.radiusVar
        if self.radius > self.max_radius:
            self.timer.stop()
            return
        self.update()

    def decRadius(self):
        self.radius -= self.radiusVar
        if self.radius < 0:
            self.timer.stop()
            return
        self.update()

    def paintEvent(self, event):
        super(RWavyButton, self).paintEvent(event)
        if self.center is None or self.is_leave and self.radius < 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush(self.full_color)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.border_radius, self.border_radius)
        painter.setClipPath(path)

        painter.drawEllipse(self.center, self.radius, self.radius)

    def enterEvent(self, event):
        self.is_leave = False
        self.center = event.position()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.incRadius)
        self.timer.start()

    def leaveEvent(self, event):
        self.is_leave = True
        self.center = self.mapFromGlobal(QCursor.pos())
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.decRadius)
        self.timer.start()

    def showEvent(self, event):
        super().showEvent(event)
        self.getStyleSheetConfig()
        self.uiConfig()
        self.animationConfig()

    def setFont(self,font:QFont):
        self.pushButton.setFont(font)

    def setText(self,text:str):
        self.pushButton.setText(text)

    def setIcon(self,icon:QIcon):
        self.pushButton.setIcon(icon)


if __name__ == '__main__':
    app = QApplication()
    w = QWidget()
    w.resize(800,800)
    w.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bd39, "
                         "stop:0.1 #00b844, stop:0.2 #00b44f, stop:0.3 #00af59, stop:0.4 #00aa64, "
                         "stop:0.5 #01a66f, stop:0.6 #01a17a, stop:0.7 #019c84, stop:0.8 #01988f, "
                         "stop:0.9 #01939a);")

    # 按钮样式配置
    btn = RWavyButton(w)
    btn.setGeometry(QRect(290, 280, 110, 35))
    btn.setStyleSheet(u"#RWavyButton{"
                       "    background-color: rgb(46, 22, 177);"
                       "	border-radius:10px;"                  # 设置圆角
                      "    R-full-color:rgb(255, 89, 0);"         # 设置填充颜色
                      "    R-font-color:White;"                   # 设置字体颜色
                      "}"
                      )

    # 设置字体
    font = QFont()
    font.setPointSize(10)
    btn.setFont(font)

    # 填写文字内容
    btn.setText(" 会变色喔")

    # 设置图标
    icon = QIcon()
    icon.addFile(u":/\u56fe\u6807/\u56fe\u6807/\u4fdd\u5b58.png", QSize(24,24), QIcon.Normal, QIcon.Off)
    btn.setIcon(icon)

    # btn.setStyleSheetConfig()

    w.show()
    app.exec()
