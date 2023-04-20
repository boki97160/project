import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout
import choose,reader 

class History(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('Select History window')
        self.resize(300,200)
        self.select_history()
    
    def select_history(self): #選擇歷史紀錄的檔案
        self.history_dir = './HistoryRecord'
        if not os.path.isdir(self.history_dir):
            os.makedirs(self.history_dir)
            
        
        self.hs_buttom = QtWidgets.QPushButton(self)
        self.hs_buttom.setGeometry(QtCore.QRect(100,70,113,32))
        self.hs_buttom.setObjectName("button")
        self.hs_buttom.setText('select history')
        self.hs_buttom.clicked.connect(self.HistoryCheck)
        
        self.notselect_buttom = QtWidgets.QPushButton(self)
        self.notselect_buttom.setGeometry(QtCore.QRect(100,100,113,32))
        self.notselect_buttom.setObjectName("button")
        self.notselect_buttom.setText('Not select history')
        self.notselect_buttom.clicked.connect(self.LeaveGUI)
       
    def HistoryCheck(self): #查看歷史紀錄
        self.notselect_buttom.deleteLater()
        if len(os.listdir(self.history_dir)) == 0: #裡面沒紀錄
            self.hs_buttom.deleteLater()
            content = 'There is no history data. Please clink "exit" buttom to choose data'
            self.text = QLabel(content,self)
            self.text.setAlignment(QtCore.Qt.AlignCenter)
            self.CloseGUI()
            
        else : 
            #filename, filetype = QFileDialog.getOpenFileName(self, "select HistoryRecord", history_dir)                
            history_folder_path = QFileDialog.getExistingDirectory(self, "select HistoryRecordFolder", "HistoryRecord")
            history_folder_path = history_folder_path.split('/')[-1]
            #print(history_folder_path)
            self.reader = reader.Reader()
            self.reader.historypath(history_folder_path)
            self.reader.getdata()
            self.reader.initUI(app)

    def CloseGUI(self): # for leave_button
        self.leave_buttom = QtWidgets.QPushButton(self)
        self.leave_buttom.setText('exit')
        self.leave_buttom.setGeometry(QtCore.QRect(200,70,113,32))
        self.leave_buttom.setObjectName("buttom")
        layout = QVBoxLayout() # let message and buttom show in GUI together
        layout.addWidget(self.text)
        layout.addWidget(self.leave_buttom)
        self.setLayout(layout)   
        self.leave_buttom.clicked.connect(self.LeaveGUI)

    def LeaveGUI(self):             # for leaving GUI and execute choose.py
        self.close()
        self.choose = choose.Choose(app)    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    history = History()
    history.show()
    sys.exit(app.exec_())