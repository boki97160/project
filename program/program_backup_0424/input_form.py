from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import json


class Input_keys:
    def __init__(self):
        pass
    def initUI(self,app):
        self.app = app
        self.form = QWidget()
        # TODO: form size
        self.form.resize(1100,800)
        self.form.show()
        
    def input_abbr(self):
        json_file = open('key_content.json','r')
        data = json.load(json_file)
        self.width = data['width']
        self.count = data['key_count']
        self.abbr_label=[]
        self.text=["" for i in range(self.count)]
        QFontDatabase.addApplicationFont("./font/Inconsolata-VariableFont_wdth,wght.ttf")
        self.titleLabel = [ QLabel(self.form) for i in range(3)]
        titleText = ["Key","Abbreviation","Stitch Change"]
        self.avai = [i for i in range(self.count)]
        
        self.imgheight= round(700/((self.count+2))*5//6)
        if self.imgheight >50:
            self.imgheight = 50
        json_file.close()
        for i in range(3):
            self.titleLabel[i].setText(titleText[i])
            self.titleLabel[i].setFont(QFont('inconsolata',12))
            self.titleLabel[i].setGeometry(10+i*350,10,300,self.imgheight*6//5)
            self.titleLabel[i].show()
        
        self.refresh()
        self.nextButton = QPushButton(self.form)
        self.nextButton.setFont(QFont('inconsolata',12))
        self.nextButton.setText('show chart')
        #self.nextButton.setGeometry(10,800-self.imgheight,100,self.imgheight*6//5)
        self.nextButton.setGeometry(10, 600, 100, self.imgheight*6//5)
        self.nextButton.clicked.connect(lambda x :self.getData())
        self.nextButton.show()
        
    def refresh(self):
        for label in self.abbr_label:
            for item in label:
                item.hide()
        self.abbr_label = []
        print(len(self.avai),len(self.width))
        for i in range(len(self.avai)):
            imgLabel = QLabel(self.form)
            pixmap = QPixmap('./'+str(self.avai[i])+'.png').scaled(self.width[i]*self.imgheight,self.imgheight)
            imgLabel.setPixmap(pixmap)
            imgLabel.setGeometry(10,(i+1)*(self.imgheight*6//5),self.width[i]*self.imgheight,self.imgheight)
            imgLabel.setStyleSheet("border: 2px solid;")
            imgLabel.show()
            textbox = QLineEdit(self.form)
            textbox.setText(self.text[i])
            textbox.setGeometry(360,(i+1)*(self.imgheight*6//5),300,self.imgheight)
            textbox.show()
            stitch_change = QSpinBox(self.form)
            stitch_change.setGeometry(710,(i+1)*(self.imgheight*6//5),100,self.imgheight)
            stitch_change.setFont(QFont('inconsolata',18))
            stitch_change.setMinimum(-5)
            stitch_change.setMaximum(5)
            stitch_change.show()
            deleteButton = QPushButton(self.form)
            deleteButton.setText("delete")
            deleteButton.setFont(QFont('inconsolata',12))
            deleteButton.setGeometry(975,(i+1)*((self.imgheight*6//5)),100,self.imgheight)
            deleteButton.show()
            self.abbr_label.append([imgLabel,textbox,stitch_change,deleteButton])
        for i in range(len(self.avai)):
            self.abbr_label[i][3].clicked.connect(lambda j,i=i : self.deleteKey(self.avai[i]+j))
    def deleteKey(self,index):
        self.text=[]
        for i in range(len(self.avai)):
            if i != self.avai.index(index):
                self.text.append(self.abbr_label[i][1].text())
        self.width.pop(self.avai.index(index))
        self.avai.remove(index)
        self.refresh()
    def getData(self):
        self.data_list = ["" for i in range(self.count)]
        self.stitch = ["0" for i in range(self.count)]
        for i in range(self.count):  
            if i in self.avai: 
                self.data_list[i] = self.abbr_label[self.avai.index(i)][1].text()
                self.stitch[i] = str(self.abbr_label[self.avai.index(i)][2].value())
        json_file = open('key_content.json','w')
        json_file.write(json.dumps({"abbr":self.data_list,"sts":self.stitch}))
        #f.write(",".join(self.data_list)+',\n')
        #f.write(",".join(self.stitch)+',\n')
        json_file.close()
        sys.exit(0)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ik = Input_keys()
    ik.initUI(app)
    ik.input_abbr()
    sys.exit(app.exec_())
    