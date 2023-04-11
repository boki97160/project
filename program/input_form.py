from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


f = open("key_content.txt","r+")

class Input_keys:
    def __init__(self):
        pass
    def initUI(self,app,key_count):
        self.app = app
        self.form = QWidget()
        # TODO: form size
        self.form.resize(1100,800)
        self.form.show()
        self.input_abbr(p)
        
    def input_abbr(self,key_count):
        self.key_count = key_count
        self.abbr_label=[]
        self.text=["" for i in range(key_count)]
        QFontDatabase.addApplicationFont("./font/Inconsolata-VariableFont_wdth,wght.ttf")
        self.titleLabel = [ QLabel(self.form) for i in range(3)]
        titleText = ["Key","Abbreviation","Stitch Change"]
        self.avai = [i for i in range(self.key_count)]
        for i in range(3):
            self.titleLabel[i].setText(titleText[i])
            self.titleLabel[i].setFont(QFont('inconsolata',18))
            self.titleLabel[i].setGeometry(10+i*350,10,300,75)
            self.titleLabel[i].show()
        self.refresh()
        self.nextButton = QPushButton(self.form)
        self.nextButton.setFont(QFont('inconsolata',12))
        self.nextButton.setGeometry(10,700,100,50)
        self.nextButton.clicked.connect(lambda x :self.getData())
        self.nextButton.show()
        
    def refresh(self):
        for label in self.abbr_label:
            for item in label:
                item.hide()
        self.abbr_label = []
        for i in range(len(self.avai)):
            imgLabel = QLabel(self.form)
            pixmap = QPixmap('./'+str(self.avai[i])+'.png').scaled(50,50)
            imgLabel.setPixmap(pixmap)
            imgLabel.setGeometry(10,100+i*75,50,50)
            imgLabel.setStyleSheet("border: 2px solid;")
            imgLabel.show()
            textbox = QLineEdit(self.form)
            textbox.setText(self.text[i])
            textbox.setGeometry(360,100+i*75,300,50)
            textbox.show()
            stitch_change = QSpinBox(self.form)
            stitch_change.setGeometry(710,100+i*75,100,50)
            stitch_change.setFont(QFont('inconsolata',18))
            stitch_change.setMinimum(-5)
            stitch_change.setMaximum(5)
            stitch_change.show()
            deleteButton = QPushButton(self.form)
            deleteButton.setText("delete")
            deleteButton.setFont(QFont('inconsolata',12))
            deleteButton.setGeometry(975,100+i*75,100,50)
            deleteButton.show()
            self.abbr_label.append([imgLabel,textbox,stitch_change,deleteButton])
        for i in range(len(self.avai)):
            self.abbr_label[i][3].clicked.connect(lambda j,i=i : self.deleteKey(self.avai[i]+j))
    def deleteKey(self,index):
        self.text=[]
        for i in range(len(self.avai)):
            if i != self.avai.index(index):
                self.text.append(self.abbr_label[i][1].text())
        self.avai.remove(index)
        self.refresh()
    def getData(self):
        self.data_list = ["" for i in range(self.key_count)]
        self.stitch = [0 for i in range(self.key_count)]
        for i in range(self.key_count):  
            if i in self.avai: 
                self.data_list[i] = self.abbr_label[self.avai.index(i)][1].text()
                self.stitch[i] = str(self.abbr_label[self.avai.index(i)][2].value())
        f.write(",".join(self.data_list)+',\n')
        f.write(",".join(self.stitch)+',\n')
        f.close()
        sys.exit(0)
if __name__ == "__main__":
    p = int(f.readline())
    app = QApplication(sys.argv)
    ik = Input_keys()
    ik.initUI(app,p)
    sys.exit(app.exec_())
    