import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore

from random import randint
import memory_management


# 加载图片资源文件
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 界面主线程
class MyWindow(QMainWindow, memory_management.Ui_MainWindow):
    # 对界面进行初始化
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        MyICO = resource_path(os.path.join("res","favicon.ico"))
        self.setWindowIcon(QIcon(MyICO))
        self.GenerateCommandButton.clicked.connect(self.GenerateCommand)
        self.ExecuteOneButton.clicked.connect(self.ExecuteOne)
        self.ExecuteFiveButton.clicked.connect(self.ExecuteFive)
        self.ExecuteAllButton.clicked.connect(self.ExecuteAll)
        self.TotalPageValue = 0
        self.PageCommandValue = 0
        self.MyCommandList = []
        self.TotalCommandValue = 0
        self.ScheduleMethod = ""
        self.MemoryAllocation = []
        self.CurrentPointer = 0
        self.FailureTimes = 0
        self.PageLackCounter.setStyleSheet("QLabel{color: green;}")
        self.PageLackText.setStyleSheet("QLabel{color: green;}")
        self.PageLackRadioText.setStyleSheet("QLabel{color: green;}")
        self.PageLackRadio.setStyleSheet("QLabel{color: green;}")    
    
    # 执行一条指令
    def ExecuteOne(self):
        self.FIFOButton.setEnabled(False)
        self.LRUButton.setEnabled(False)
        self.TotalCommand.setEnabled(False)
        self.PageCommand.setEnabled(False)
        self.TotalPage.setEnabled(False)
        self.GenerateCommandButton.setEnabled(False)
        self.Execute()
        if self.CheckEnd():
            return       
     
    #  执行五条指令   
    def ExecuteFive(self):
        self.FIFOButton.setEnabled(False)
        self.LRUButton.setEnabled(False)
        self.TotalCommand.setEnabled(False)
        self.PageCommand.setEnabled(False)
        self.TotalPage.setEnabled(False)
        self.GenerateCommandButton.setEnabled(False)    
        for i in range(5):     
            self.Execute()
            if self.CheckEnd():
                break               

    #  执行全部指令          
    def ExecuteAll(self):
        self.FIFOButton.setEnabled(False)
        self.LRUButton.setEnabled(False)
        self.TotalCommand.setEnabled(False)
        self.PageCommand.setEnabled(False)
        self.TotalPage.setEnabled(False)
        self.GenerateCommandButton.setEnabled(False)    
        while(True):        
            self.Execute()
            if self.CheckEnd():
                break
    
    # 执行指令
    def Execute(self):
        page = self.MyCommandList[self.CurrentPointer] // self.PageCommandValue
        item = "第" + str(self.CurrentPointer) + "条指令的逻辑地址为" + str(self.MyCommandList[self.CurrentPointer]) + \
        "，所在页面为第" + str(page) + "页。"
        if page in self.MemoryAllocation:
            item += "在内存中找到该页面。"
            # 通过列表中页面排序来实现LRU，FIFO是自动的，无需额外代码
            if self.ScheduleMethod == "LRU":
                self.MemoryAllocation.remove(page)
                self.MemoryAllocation.append(page)
        else:
            self.FailureTimes += 1
            item += "将第" + str(page) + "页调入内存"
            if len(self.MemoryAllocation) < self.TotalPageValue:
                self.MemoryAllocation.append(page)
                item += "。"
            else:
                item += "，并将第" + str(self.MemoryAllocation[0]) + "页置换出内存。"
                del(self.MemoryAllocation[0])
                self.MemoryAllocation.append(page)
        self.PageLackCounter.setText(str(self.FailureTimes))
        self.PageLackRadio.setText(str(round(self.FailureTimes / (self.CurrentPointer + 1), 3)))
        if self.FailureTimes > 0:
            self.PageLackCounter.setStyleSheet("QLabel{color: red;}")
            self.PageLackText.setStyleSheet("QLabel{color: red;}")
            self.PageLackRadioText.setStyleSheet("QLabel{color: red;}")
            self.PageLackRadio.setStyleSheet("QLabel{color: red;}")            
        self.CommandLog.addItem(item)
        self.CurrentPointer += 1

    # 检查是否已经运行完全部指令                
    def CheckEnd(self):
        if(self.CurrentPointer < self.TotalCommandValue):
            return False
        self.ExecuteOneButton.setEnabled(False)
        self.ExecuteFiveButton.setEnabled(False)
        self.ExecuteAllButton.setEnabled(False)            
        self.FIFOButton.setEnabled(True)
        self.LRUButton.setEnabled(True)
        self.TotalCommand.setEnabled(True)
        self.PageCommand.setEnabled(True)
        self.TotalPage.setEnabled(True)  
        self.GenerateCommandButton.setEnabled(True)
        QMessageBox.information(self, '模拟结束', '全部指令运行完成！')
        return True

    # 随机生成所需指令    
    def GenerateCommand(self):
        self.PageLackCounter.setText(str(0))
        self.PageLackRadio.setText(str(0))
        self.PageLackCounter.setStyleSheet("QLabel{color: green;}")
        self.PageLackText.setStyleSheet("QLabel{color: green;}")
        self.PageLackRadioText.setStyleSheet("QLabel{color: green;}")
        self.PageLackRadio.setStyleSheet("QLabel{color: green;}")    
        self.CommandList.clear()
        self.CommandLog.clear()
        self.MyCommandList = []
        self.MemoryAllocation = []
        self.CurrentPointer = 0
        self.FailureTimes = 0
        if self.FIFOButton.isChecked():
            self.ScheduleMethod = "FIFO"
        else:
            self.ScheduleMethod = "LRU"
        self.TotalPageValue = self.TotalPage.value()
        self.PageCommandValue = self.PageCommand.value()
        self.TotalCommandValue = self.TotalCommand.value()
        start_point = randint(self.TotalCommandValue//3, self.TotalCommandValue * 2//3)
        pointer = 1
        self.MyCommandList.append(start_point)
        pointer += 1
        # 按PPT中描述的方式生成
        if pointer <= self.TotalCommandValue:
            self.MyCommandList.append(start_point + 1)
            pointer += 1            
        while True:
            if pointer > self.TotalCommandValue:
                break         
            temp = randint(0, start_point - 1)
            self.MyCommandList.append(temp)
            pointer += 1
            if pointer > self.TotalCommandValue:
                break
            self.MyCommandList.append(temp + 1)
            pointer += 1
            if pointer > self.TotalCommandValue:
                break            
            temp = randint(start_point + 1, self.TotalCommandValue - 2)
            self.MyCommandList.append(temp)
            pointer += 1
            if pointer > self.TotalCommandValue:
                break
            self.MyCommandList.append(temp + 1)
            pointer += 1             
        for i in range(self.TotalCommandValue):
            item = str(i)
            while len(item) < 5:
                item += " "
            item += "\t"
            item += str(self.MyCommandList[i])
            self.CommandList.addItem(item)
        self.ExecuteOneButton.setEnabled(True)
        self.ExecuteFiveButton.setEnabled(True)
        self.ExecuteAllButton.setEnabled(True)
        QMessageBox.information(self, '生成结束', '指令序列生成成功！')
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec())    
