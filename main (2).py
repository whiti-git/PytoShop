from PyQt5.QtCore import Qt , QSize  , QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
from PIL import Image, ImageFilter , ImageEnhance
app = QApplication([])
font = QFont("IBM Plex Mono")
app.setFont(font , 'QLabel')

class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background: #2e2e2e; border: 1px solid #2e2e2e; border-radius: 90px;')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('PytoShop')


win = Win()

ip = 0

result = []
workdir = ''
temp = ''


class Button(QPushButton):
    def __init__(self, text , height = 50 , width = 80):
        super().__init__(text)
        style = "background: #ff9100; border: 2px solid #8c5206; width: {}; height: {}; font-size: 20px;border-radius: 10px;".format(width , height)
        self.setStyleSheet(style)
        self.text = text
        font = QFont("IBM Plex Mono")
        self.setFont(font)

class List(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background: #ff9100;width: 60; border-radius: 10px;')


        

class Item(QListWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.text = text
        self.setTextAlignment(Qt.AlignCenter)


class Title(QWidget):
    def __init__(self, text , parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.title = QLabel(text)
        self.close = Button('❌' , 30 , 30)
        self.sclose = Button('—' , 30 , 30)
        self.title.setStyleSheet('font-size: 20px; color: white;')
        self.layout.addWidget(self.sclose , alignment=Qt.AlignLeft)
        self.layout.addWidget(self.title , alignment=Qt.AlignCenter)
        self.layout.addWidget(self.close , alignment=Qt.AlignRight)
        self.close.clicked.connect(self.closee)
        self.sclose.clicked.connect(self.sclo)
        self.setLayout(self.layout)
        self.start = QPoint(0, 0)
        self.pressing = False
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.move(self.end.x() - self.parent.width()/2, self.end.y() - 20)
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def closee(self):
        self.parent.close()
        quit()
    
    def sclo(self):
        self.parent.showMinimized()



        
main = QVBoxLayout()
main.addWidget(Title('PytoShop' , win))
top = QHBoxLayout()
main.addLayout(top)
line1 = QVBoxLayout()
line2 = QVBoxLayout()
line3 = QVBoxLayout()
top.addLayout(line1)
top.addLayout(line2)
top.addLayout(line3)

PList = List()
Fdialog = QFileDialog()
Fdialog.setOptions(QFileDialog.ShowDirsOnly)
FButton = Button('Open' , 20 , 100)


line1.addWidget(FButton)
line1.addWidget(PList)

Photo = QLabel('')

line2.addWidget(Photo)

Bleft = Button('Left')
BBlur = Button('Blur')
BMirror = Button('Mirror')
BContrast = Button('Contrast')
BWb = Button('W/B')

line3.addWidget(Bleft)
line3.addWidget(BMirror)
line3.addWidget(BBlur)
line3.addWidget(BContrast)
line3.addWidget(BWb)

def dir():
    global workdir
    workdir = Fdialog.getExistingDirectory()
    print(workdir)
    filter()

def click():
    global temp , workdir , ip
    ip = ImageProcessor(PList.currentItem().text)
    ip.open(workdir)
    ip.show(Photo)
    bind()
def bind():
    BBlur.clicked.connect(ip.blur)
    Bleft.clicked.connect(ip.left)
    BContrast.clicked.connect(ip.Cont)
    BMirror.clicked.connect(ip.Mirro)
    BWb.clicked.connect(ip.Wb)


def filter():
    global result , workdir
    temp = os.listdir(workdir)
    PList.clear()
    for i in temp:
        if i.endswith(".png"):
            result.append(i)
            temp = Item(i)
            
            PList.addItem(temp)
        else:
            pass


class ImageProcessor():
    def __init__(self , filename):
        self.filename = filename
        self.save_dir = '/Modified//'
    def open(self, workdir):
        self.workdir = workdir
        path = os.path.join(workdir,self.filename)
        self.path = path
        self.image = Image.open(path)
    
    def show(self , image = Photo):
        self.im = image
        image.hide()
        pix = QPixmap(self.path)
        pix = pix.scaled(400, 550, Qt.KeepAspectRatio)
        image.setPixmap(pix)
        image.show()
    


    def show_m(self):
        self.im.hide()
        pix = QPixmap(self.m_p)
        pix = pix.scaled(400, 550, Qt.KeepAspectRatio)
        self.im.setPixmap(pix)
        self.im.show()

    def left(self):
        left = self.image.transpose(Image.ROTATE_90)
        self.image = left
        self.m_p = self.workdir + self.save_dir + self.filename
        try:
            left.save(self.m_p)
        except:
            os.mkdir(self.workdir + self.save_dir)
            left.save(self.m_p)
        self.show_m()


    def Wb(self):
        wb = self.image.convert('L')
        self.image = wb
        self.m_p = self.workdir + self.save_dir + self.filename
        try:
            wb.save(self.m_p)
        except:
            os.mkdir(self.workdir + self.save_dir)
            wb.save(self.m_p)
        self.show_m()

    def blur(self):
        left = self.image.filter(ImageFilter.BLUR)
        self.image = left
        self.m_p = self.workdir + self.save_dir + self.filename
        try:
            left.save(self.m_p)
        except:
            os.mkdir(self.workdir + self.save_dir)
            left.save(self.m_p)
        self.show_m()

    def Mirro(self):
        left = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.image = left
        self.m_p = self.workdir + self.save_dir + self.filename
        try:
            left.save(self.m_p)
        except:
            os.mkdir(self.workdir + self.save_dir)
            left.save(self.m_p)
        self.show_m()

    def Cont(self):
        left = ImageEnhance.Contrast(self.image)
        left = left.enhance(1.5)
        self.image = left
        self.m_p = self.workdir +self.save_dir + self.filename
        try:
            left.save(self.m_p)
        except:
            os.mkdir(self.workdir + self.save_dir)
            left.save(self.m_p)
        self.show_m()

FButton.clicked.connect(dir)
PList.clicked.connect(click)
win.show()
win.resize(600 , 600)
win.setLayout(main)

app.exec_()