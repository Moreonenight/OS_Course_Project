# -*- coding: utf-8 -*-
# 重复的代码可能特别多，因为不少代码是程序生成的

import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QGraphicsView
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, QPoint
from time import sleep

import Elevator

PIC_CHANGE_INTERVAL = 4
PIC_MOVE_INTERVAL = 4
FULL_LENGTH_LABEL = 95 * PIC_MOVE_INTERVAL
TICK_TIME = 50

# 加载图片资源文件
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MyElevator(QGraphicsView):
    def __init__(self, MainWindow):
        super(MyElevator, self).__init__(MainWindow)
        self.state = 0 #0代表静止，1代表上行，2代表下行
        self.door_state = 0 # 电梯门打开程度
        self.door_open = False # 是否要打开电梯门
        self.position = 0 # 电梯位置
        self.myList = [] # 上下行列表
        self.level = 1 # 电梯楼层
        
    def DecidePosition(self, btn, label, pos):  # 决定电梯控件应该绘制的位置      
        tmp_y = label.mapToGlobal(QPoint(0,0)).y() - pos.y()  + (label.height() - btn.height()) * (FULL_LENGTH_LABEL - self.position) // FULL_LENGTH_LABEL
        self.resize(label.width(), btn.height())
        self.move(label.mapToGlobal(QPoint(0,0)).x() - pos.x(), tmp_y)
    
    def Calc_Distance(self, calc_level, is_up): # 计算距离，调度算法会用到
        max_level = 0
        min_level = 40
        for p in self.myList:
            if p > max_level:
                max_level = p
            if p < min_level:
                min_level = p
        if max_level < self.level:
            max_level = self.level
        if min_level > self.level:
            min_level = self.level            
        if self.state == 0:
            return abs(self.level - calc_level)
        elif self.state == 1:
            if is_up == True and self.level - calc_level < 0:
                return abs(self.level - calc_level)
            elif is_up == True:
                return max(2 * (max_level - min_level)- abs(self.level - calc_level), 2 * max_level - self.level - calc_level)
            else:
                return 2 * max_level - self.level - calc_level
        else:
            if is_up != True and self.level - calc_level > 0:
                return abs(self.level - calc_level)
            elif is_up != True:
                return max(2 * (max_level - min_level)- abs(self.level - calc_level),self.level + calc_level - 2 * min_level )
            else:
                return self.level + calc_level - 2 * min_level             
# 窗口类，注意以下有大量代码是生成的，可读性很差
class MyWindow(QMainWindow, Elevator.Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('电梯调度')
        MyICO = resource_path(os.path.join("res","favicon.ico"))
        self.setWindowIcon(QIcon(MyICO))
        self.pushButton_1_warning.clicked.connect(self.handleWarning)
        self.pushButton_2_warning.clicked.connect(self.handleWarning)
        self.pushButton_3_warning.clicked.connect(self.handleWarning)
        self.pushButton_4_warning.clicked.connect(self.handleWarning)
        self.pushButton_5_warning.clicked.connect(self.handleWarning)
        self.WarningCount = 0
        self.MyUpPic = resource_path(os.path.join("res","up.png")).replace("\\", "/")
        self.MyDownPic = resource_path(os.path.join("res","down.png")).replace("\\", "/")
        self.MyClosedPic = resource_path(os.path.join("res","closed.png")).replace("\\", "/")
        self.MyNarrowPic = resource_path(os.path.join("res","narrow_open.png")).replace("\\", "/")
        self.MyWidePic = resource_path(os.path.join("res","wide_open.png")).replace("\\", "/")
        self.MyOpenPic = resource_path(os.path.join("res","open.png")).replace("\\", "/")
        self.elevator_list = []
        for i in range(5):
            self.elevator_list.append(MyElevator(self))
        self.timer = QTimer()
        self.timer.timeout.connect(self.TickUpdate)
        self.timer.start(TICK_TIME)
    
    def DispatchUpdate(self):
        if self.pushButton_1_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(1, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(1, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(1, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(1)
        if self.pushButton_2_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(2, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(2, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(2, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(2)
        if self.pushButton_3_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(3, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(3, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(3, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(3)
        if self.pushButton_4_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(4, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(4, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(4, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(4)
        if self.pushButton_5_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(5, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(5, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(5, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(5)
        if self.pushButton_6_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(6, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(6, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(6, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(6)
        if self.pushButton_7_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(7, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(7, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(7, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(7)
        if self.pushButton_8_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(8, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(8, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(8, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(8)
        if self.pushButton_9_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(9, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(9, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(9, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(9)
        if self.pushButton_10_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(10, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(10, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(10, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(10)
        if self.pushButton_11_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(11, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(11, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(11, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(11)
        if self.pushButton_12_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(12, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(12, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(12, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(12)
        if self.pushButton_13_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(13, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(13, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(13, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(13)
        if self.pushButton_14_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(14, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(14, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(14, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(14)
        if self.pushButton_15_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(15, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(15, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(15, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(15)
        if self.pushButton_16_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(16, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(16, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(16, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(16)
        if self.pushButton_17_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(17, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(17, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(17, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(17)
        if self.pushButton_18_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(18, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(18, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(18, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(18)
        if self.pushButton_19_up.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(19, True)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(19, True) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(19, True)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(19)
        if self.pushButton_2_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(2, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(2, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(2, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(2)
        if self.pushButton_3_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(3, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(3, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(3, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(3)
        if self.pushButton_4_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(4, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(4, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(4, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(4)
        if self.pushButton_5_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(5, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(5, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(5, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(5)
        if self.pushButton_6_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(6, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(6, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(6, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(6)
        if self.pushButton_7_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(7, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(7, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(7, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(7)
        if self.pushButton_8_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(8, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(8, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(8, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(8)
        if self.pushButton_9_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(9, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(9, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(9, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(9)
        if self.pushButton_10_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(10, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(10, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(10, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(10)
        if self.pushButton_11_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(11, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(11, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(11, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(11)
        if self.pushButton_12_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(12, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(12, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(12, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(12)
        if self.pushButton_13_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(13, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(13, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(13, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(13)
        if self.pushButton_14_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(14, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(14, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(14, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(14)
        if self.pushButton_15_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(15, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(15, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(15, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(15)
        if self.pushButton_16_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(16, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(16, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(16, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(16)
        if self.pushButton_17_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(17, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(17, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(17, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(17)
        if self.pushButton_18_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(18, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(18, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(18, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(18)
        if self.pushButton_19_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(19, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(19, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(19, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(19)
        if self.pushButton_20_down.isChecked():
            tmp = self.elevator_list[0].Calc_Distance(20, False)
            tmp_i = 0
            for i in range(1, 5):
                if self.elevator_list[i].Calc_Distance(20, False) < tmp:
                    tmp = self.elevator_list[i].Calc_Distance(20, False)
                    tmp_i = i
            self.elevator_list[tmp_i].myList.append(20)
        if self.elevator_list[0].position % (5 * PIC_MOVE_INTERVAL) == 0 and self.elevator_list[0].door_state != 0:   
            if self.elevator_list[0].state != -1 and self.elevator_list[0].level != 20:
                for i in range(5):
                    if i != 0:
                        if self.elevator_list[0].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[0].level)
            if self.elevator_list[0].state != 1 and self.elevator_list[0].level != 1:
                for i in range(5):
                    if i != 0:
                        if self.elevator_list[0].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[0].level)
            for l in self.elevator_list[0].myList:
                if l > self.elevator_list[0].level:
                    pass
            else:
                if self.elevator_list[0].level != 1:
                    for i in range(5):
                        if i != 0:
                            if self.elevator_list[0].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[0].level)
            for l in self.elevator_list[0].myList:
                if l < self.elevator_list[0].level:
                    pass
            else:
                if self.elevator_list[0].level != 20:
                    for i in range(5):
                        if i != 0:
                            if self.elevator_list[0].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[0].level)
        if self.elevator_list[1].position % (5 * PIC_MOVE_INTERVAL) == 0 and self.elevator_list[1].door_state != 0:
            if self.elevator_list[1].state != -1 and self.elevator_list[1].level != 20:
                for i in range(5):
                    if i != 1:
                        if self.elevator_list[1].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[1].level)
            if self.elevator_list[1].state != 1 and self.elevator_list[1].level != 1:
                for i in range(5):
                    if i != 1:
                        if self.elevator_list[1].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[1].level)
            for l in self.elevator_list[1].myList:
                if l > self.elevator_list[1].level:
                    pass
            else:
                if self.elevator_list[1].level != 1:
                    for i in range(5):
                        if i != 1:
                            if self.elevator_list[1].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[1].level)
            for l in self.elevator_list[1].myList:
                if l < self.elevator_list[1].level:
                    pass
            else:
                if self.elevator_list[1].level != 20:
                    for i in range(5):
                        if i != 1:
                            if self.elevator_list[1].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[1].level)
        if self.elevator_list[2].position % (5 * PIC_MOVE_INTERVAL) == 0 and self.elevator_list[2].door_state != 0:
            if self.elevator_list[2].state != -1 and self.elevator_list[2].level != 20:
                for i in range(5):
                    if i != 2:
                        if self.elevator_list[2].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[2].level)
            if self.elevator_list[2].state != 1 and self.elevator_list[2].level != 1:
                for i in range(5):
                    if i != 2:
                        if self.elevator_list[2].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[2].level)
            for l in self.elevator_list[2].myList:
                if l > self.elevator_list[2].level:
                    pass
            else:
                if self.elevator_list[2].level != 1:
                    for i in range(5):
                        if i != 2:
                            if self.elevator_list[2].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[2].level)
            for l in self.elevator_list[2].myList:
                if l < self.elevator_list[2].level:
                    pass
            else:
                if self.elevator_list[2].level != 20:
                    for i in range(5):
                        if i != 2:
                            if self.elevator_list[2].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[2].level)
        if self.elevator_list[3].position % (5 * PIC_MOVE_INTERVAL) == 0 and self.elevator_list[3].door_state != 0:
            if self.elevator_list[3].state != -1 and self.elevator_list[3].level != 20:
                for i in range(5):
                    if i != 3:
                        if self.elevator_list[3].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[3].level)
            if self.elevator_list[3].state != 1 and self.elevator_list[3].level != 1:
                for i in range(5):
                    if i != 3:
                        if self.elevator_list[3].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[3].level)
            for l in self.elevator_list[3].myList:
                if l > self.elevator_list[3].level:
                    pass
            else:
                if self.elevator_list[3].level != 1:
                    for i in range(5):
                        if i != 3:
                            if self.elevator_list[3].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[3].level)
            for l in self.elevator_list[3].myList:
                if l < self.elevator_list[3].level:
                    pass
            else:
                if self.elevator_list[3].level != 20:
                    for i in range(5):
                        if i != 3:
                            if self.elevator_list[3].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[3].level)
        if self.elevator_list[4].position % (5 * PIC_MOVE_INTERVAL) == 0 and self.elevator_list[4].door_state != 0:
            if self.elevator_list[4].state != -1 and self.elevator_list[4].level != 20:
                for i in range(5):
                    if i != 4:
                        if self.elevator_list[4].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[4].level)
            if self.elevator_list[4].state != 1 and self.elevator_list[4].level != 1:
                for i in range(5):
                    if i != 4:
                        if self.elevator_list[4].level in self.elevator_list[i].myList:
                            self.elevator_list[i].myList.remove(self.elevator_list[4].level)
            for l in self.elevator_list[4].myList:
                if l > self.elevator_list[4].level:
                    pass
            else:
                if self.elevator_list[4].level != 1:
                    for i in range(5):
                        if i != 4:
                            if self.elevator_list[4].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[4].level)
            for l in self.elevator_list[4].myList:
                if l < self.elevator_list[4].level:
                    pass
            else:
                if self.elevator_list[4].level != 20:
                    for i in range(5):
                        if i != 4:
                            if self.elevator_list[4].level in self.elevator_list[i].myList:
                                self.elevator_list[i].myList.remove(self.elevator_list[4].level)
             
    def ListUpdate(self):
        if self.pushButton_1_1.isChecked():
            self.elevator_list[0].myList.append(1)
        if self.pushButton_1_2.isChecked():
            self.elevator_list[0].myList.append(2)
        if self.pushButton_1_3.isChecked():
            self.elevator_list[0].myList.append(3)
        if self.pushButton_1_4.isChecked():
            self.elevator_list[0].myList.append(4)
        if self.pushButton_1_5.isChecked():
            self.elevator_list[0].myList.append(5)
        if self.pushButton_1_6.isChecked():
            self.elevator_list[0].myList.append(6)
        if self.pushButton_1_7.isChecked():
            self.elevator_list[0].myList.append(7)
        if self.pushButton_1_8.isChecked():
            self.elevator_list[0].myList.append(8)
        if self.pushButton_1_9.isChecked():
            self.elevator_list[0].myList.append(9)
        if self.pushButton_1_10.isChecked():
            self.elevator_list[0].myList.append(10)
        if self.pushButton_1_11.isChecked():
            self.elevator_list[0].myList.append(11)
        if self.pushButton_1_12.isChecked():
            self.elevator_list[0].myList.append(12)
        if self.pushButton_1_13.isChecked():
            self.elevator_list[0].myList.append(13)
        if self.pushButton_1_14.isChecked():
            self.elevator_list[0].myList.append(14)
        if self.pushButton_1_15.isChecked():
            self.elevator_list[0].myList.append(15)
        if self.pushButton_1_16.isChecked():
            self.elevator_list[0].myList.append(16)
        if self.pushButton_1_17.isChecked():
            self.elevator_list[0].myList.append(17)
        if self.pushButton_1_18.isChecked():
            self.elevator_list[0].myList.append(18)
        if self.pushButton_1_19.isChecked():
            self.elevator_list[0].myList.append(19)
        if self.pushButton_1_20.isChecked():
            self.elevator_list[0].myList.append(20)            
        
        if self.pushButton_2_1.isChecked():
            self.elevator_list[1].myList.append(1)
        if self.pushButton_2_2.isChecked():
            self.elevator_list[1].myList.append(2)
        if self.pushButton_2_3.isChecked():
            self.elevator_list[1].myList.append(3)
        if self.pushButton_2_4.isChecked():
            self.elevator_list[1].myList.append(4)
        if self.pushButton_2_5.isChecked():
            self.elevator_list[1].myList.append(5)
        if self.pushButton_2_6.isChecked():
            self.elevator_list[1].myList.append(6)
        if self.pushButton_2_7.isChecked():
            self.elevator_list[1].myList.append(7)
        if self.pushButton_2_8.isChecked():
            self.elevator_list[1].myList.append(8)
        if self.pushButton_2_9.isChecked():
            self.elevator_list[1].myList.append(9)
        if self.pushButton_2_10.isChecked():
            self.elevator_list[1].myList.append(10)
        if self.pushButton_2_11.isChecked():
            self.elevator_list[1].myList.append(11)
        if self.pushButton_2_12.isChecked():
            self.elevator_list[1].myList.append(12)
        if self.pushButton_2_13.isChecked():
            self.elevator_list[1].myList.append(13)
        if self.pushButton_2_14.isChecked():
            self.elevator_list[1].myList.append(14)
        if self.pushButton_2_15.isChecked():
            self.elevator_list[1].myList.append(15)
        if self.pushButton_2_16.isChecked():
            self.elevator_list[1].myList.append(16)
        if self.pushButton_2_17.isChecked():
            self.elevator_list[1].myList.append(17)
        if self.pushButton_2_18.isChecked():
            self.elevator_list[1].myList.append(18)
        if self.pushButton_2_19.isChecked():
            self.elevator_list[1].myList.append(19)
        if self.pushButton_2_20.isChecked():
            self.elevator_list[1].myList.append(20)        

        if self.pushButton_3_1.isChecked():
            self.elevator_list[2].myList.append(1)
        if self.pushButton_3_2.isChecked():
            self.elevator_list[2].myList.append(2)
        if self.pushButton_3_3.isChecked():
            self.elevator_list[2].myList.append(3)
        if self.pushButton_3_4.isChecked():
            self.elevator_list[2].myList.append(4)
        if self.pushButton_3_5.isChecked():
            self.elevator_list[2].myList.append(5)
        if self.pushButton_3_6.isChecked():
            self.elevator_list[2].myList.append(6)
        if self.pushButton_3_7.isChecked():
            self.elevator_list[2].myList.append(7)
        if self.pushButton_3_8.isChecked():
            self.elevator_list[2].myList.append(8)
        if self.pushButton_3_9.isChecked():
            self.elevator_list[2].myList.append(9)
        if self.pushButton_3_10.isChecked():
            self.elevator_list[2].myList.append(10)
        if self.pushButton_3_11.isChecked():
            self.elevator_list[2].myList.append(11)
        if self.pushButton_3_12.isChecked():
            self.elevator_list[2].myList.append(12)
        if self.pushButton_3_13.isChecked():
            self.elevator_list[2].myList.append(13)
        if self.pushButton_3_14.isChecked():
            self.elevator_list[2].myList.append(14)
        if self.pushButton_3_15.isChecked():
            self.elevator_list[2].myList.append(15)
        if self.pushButton_3_16.isChecked():
            self.elevator_list[2].myList.append(16)
        if self.pushButton_3_17.isChecked():
            self.elevator_list[2].myList.append(17)
        if self.pushButton_3_18.isChecked():
            self.elevator_list[2].myList.append(18)
        if self.pushButton_3_19.isChecked():
            self.elevator_list[2].myList.append(19)
        if self.pushButton_3_20.isChecked():
            self.elevator_list[2].myList.append(20)

        if self.pushButton_4_1.isChecked():
            self.elevator_list[3].myList.append(1)
        if self.pushButton_4_2.isChecked():
            self.elevator_list[3].myList.append(2)
        if self.pushButton_4_3.isChecked():
            self.elevator_list[3].myList.append(3)
        if self.pushButton_4_4.isChecked():
            self.elevator_list[3].myList.append(4)
        if self.pushButton_4_5.isChecked():
            self.elevator_list[3].myList.append(5)
        if self.pushButton_4_6.isChecked():
            self.elevator_list[3].myList.append(6)
        if self.pushButton_4_7.isChecked():
            self.elevator_list[3].myList.append(7)
        if self.pushButton_4_8.isChecked():
            self.elevator_list[3].myList.append(8)
        if self.pushButton_4_9.isChecked():
            self.elevator_list[3].myList.append(9)
        if self.pushButton_4_10.isChecked():
            self.elevator_list[3].myList.append(10)
        if self.pushButton_4_11.isChecked():
            self.elevator_list[3].myList.append(11)
        if self.pushButton_4_12.isChecked():
            self.elevator_list[3].myList.append(12)
        if self.pushButton_4_13.isChecked():
            self.elevator_list[3].myList.append(13)
        if self.pushButton_4_14.isChecked():
            self.elevator_list[3].myList.append(14)
        if self.pushButton_4_15.isChecked():
            self.elevator_list[3].myList.append(15)
        if self.pushButton_4_16.isChecked():
            self.elevator_list[3].myList.append(16)
        if self.pushButton_4_17.isChecked():
            self.elevator_list[3].myList.append(17)
        if self.pushButton_4_18.isChecked():
            self.elevator_list[3].myList.append(18)
        if self.pushButton_4_19.isChecked():
            self.elevator_list[3].myList.append(19)
        if self.pushButton_4_20.isChecked():
            self.elevator_list[3].myList.append(20)

        if self.pushButton_5_1.isChecked():
            self.elevator_list[4].myList.append(1)
        if self.pushButton_5_2.isChecked():
            self.elevator_list[4].myList.append(2)
        if self.pushButton_5_3.isChecked():
            self.elevator_list[4].myList.append(3)
        if self.pushButton_5_4.isChecked():
            self.elevator_list[4].myList.append(4)
        if self.pushButton_5_5.isChecked():
            self.elevator_list[4].myList.append(5)
        if self.pushButton_5_6.isChecked():
            self.elevator_list[4].myList.append(6)
        if self.pushButton_5_7.isChecked():
            self.elevator_list[4].myList.append(7)
        if self.pushButton_5_8.isChecked():
            self.elevator_list[4].myList.append(8)
        if self.pushButton_5_9.isChecked():
            self.elevator_list[4].myList.append(9)
        if self.pushButton_5_10.isChecked():
            self.elevator_list[4].myList.append(10)
        if self.pushButton_5_11.isChecked():
            self.elevator_list[4].myList.append(11)
        if self.pushButton_5_12.isChecked():
            self.elevator_list[4].myList.append(12)
        if self.pushButton_5_13.isChecked():
            self.elevator_list[4].myList.append(13)
        if self.pushButton_5_14.isChecked():
            self.elevator_list[4].myList.append(14)
        if self.pushButton_5_15.isChecked():
            self.elevator_list[4].myList.append(15)
        if self.pushButton_5_16.isChecked():
            self.elevator_list[4].myList.append(16)
        if self.pushButton_5_17.isChecked():
            self.elevator_list[4].myList.append(17)
        if self.pushButton_5_18.isChecked():
            self.elevator_list[4].myList.append(18)
        if self.pushButton_5_19.isChecked():
            self.elevator_list[4].myList.append(19)
        if self.pushButton_5_20.isChecked():
            self.elevator_list[4].myList.append(20)
            
    def StateUpdate(self):
        self.elevator_list[0].myList = list(set(self.elevator_list[0].myList))
        self.elevator_list[1].myList = list(set(self.elevator_list[1].myList))
        self.elevator_list[2].myList = list(set(self.elevator_list[2].myList))
        self.elevator_list[3].myList = list(set(self.elevator_list[3].myList))
        self.elevator_list[4].myList = list(set(self.elevator_list[4].myList))
        
        if self.elevator_list[0].position % (5 * PIC_MOVE_INTERVAL) != 0:
            if self.elevator_list[0].state == 1:
                self.elevator_list[0].position += 1
            else:
                self.elevator_list[0].position -= 1
        else:
            if self.elevator_list[0].level in self.elevator_list[0].myList:
                self.elevator_list[0].door_open = True
                eval("self.pushButton_1_"+ str(self.elevator_list[0].level) + ".setChecked(False)")                    
                self.pushButton_1_open.setChecked(False)
                self.elevator_list[0].myList.remove(self.elevator_list[0].level)
            if self.elevator_list[0].door_open == False and self.elevator_list[0].door_state == 0:
                if self.elevator_list[0].state != -1:
                    for l in self.elevator_list[0].myList:
                        if l > self.elevator_list[0].level:
                            self.elevator_list[0].state = 1
                            self.elevator_list[0].position += 1
                            break
                    else:
                        self.elevator_list[0].state = 0
                        
                if self.elevator_list[0].state != 1:
                    for l in self.elevator_list[0].myList:
                        if l < self.elevator_list[0].level:
                            self.elevator_list[0].state = -1
                            self.elevator_list[0].position -= 1
                            break
                    else:
                        self.elevator_list[0].state = 0
            if self.elevator_list[0].door_state != 0:
                if self.elevator_list[0].state != -1 and self.elevator_list[0].level != 20:
                    eval("self.pushButton_"+ str(self.elevator_list[0].level) + "_up.setChecked(False)")
                if self.elevator_list[0].state != 1 and self.elevator_list[0].level != 1:
                    eval("self.pushButton_"+ str(self.elevator_list[0].level) + "_down.setChecked(False)")
                for l in self.elevator_list[0].myList:
                    if l > self.elevator_list[0].level:
                        pass
                else:
                    if self.elevator_list[0].level != 1:
                        eval("self.pushButton_"+ str(self.elevator_list[0].level) + "_down.setChecked(False)")
                for l in self.elevator_list[0].myList:
                    if l < self.elevator_list[0].level:
                        pass
                else:
                    if self.elevator_list[0].level != 20:
                        eval("self.pushButton_"+ str(self.elevator_list[0].level) + "_up.setChecked(False)")
                    
        if self.elevator_list[1].position % (5 * PIC_MOVE_INTERVAL) != 0:
            if self.elevator_list[1].state == 1:
                self.elevator_list[1].position += 1
            else:
                self.elevator_list[1].position -= 1
        else:
            if self.elevator_list[1].level in self.elevator_list[1].myList:
                self.elevator_list[1].door_open = True
                eval("self.pushButton_2_"+ str(self.elevator_list[1].level) + ".setChecked(False)")               
                self.pushButton_2_open.setChecked(False)
                self.elevator_list[1].myList.remove(self.elevator_list[1].level)
            if self.elevator_list[1].door_open == False and self.elevator_list[1].door_state == 0:
                if self.elevator_list[1].state != -1:
                    for l in self.elevator_list[1].myList:
                        if l > self.elevator_list[1].level:
                            self.elevator_list[1].state = 1
                            self.elevator_list[1].position += 1
                            break
                    else:
                        self.elevator_list[1].state = 0
                        
                if self.elevator_list[1].state != 1:
                    for l in self.elevator_list[1].myList:
                        if l < self.elevator_list[1].level:
                            self.elevator_list[1].state = -1
                            self.elevator_list[1].position -= 1
                            break
                    else:
                        self.elevator_list[1].state = 0
            if self.elevator_list[1].door_state != 0:            
                if self.elevator_list[1].state != -1 and self.elevator_list[1].level != 20:
                    eval("self.pushButton_"+ str(self.elevator_list[1].level) + "_up.setChecked(False)")
                if self.elevator_list[1].state != 1 and self.elevator_list[1].level != 1:
                    eval("self.pushButton_"+ str(self.elevator_list[1].level) + "_down.setChecked(False)")
                for l in self.elevator_list[1].myList:
                    if l > self.elevator_list[1].level:
                        pass
                else:
                    if self.elevator_list[1].level != 1:
                        eval("self.pushButton_"+ str(self.elevator_list[1].level) + "_down.setChecked(False)")
                for l in self.elevator_list[1].myList:
                    if l < self.elevator_list[1].level:
                        pass
                else:
                    if self.elevator_list[1].level != 20:
                        eval("self.pushButton_"+ str(self.elevator_list[1].level) + "_up.setChecked(False)")                

        if self.elevator_list[2].position % (5 * PIC_MOVE_INTERVAL) != 0:
            if self.elevator_list[2].state == 1:
                self.elevator_list[2].position += 1
            else:
                self.elevator_list[2].position -= 1
        else:
            if self.elevator_list[2].level in self.elevator_list[2].myList:
                self.elevator_list[2].door_open = True
                eval("self.pushButton_3_"+ str(self.elevator_list[2].level) + ".setChecked(False)")                 
                self.pushButton_3_open.setChecked(False)
                self.elevator_list[2].myList.remove(self.elevator_list[2].level)
            if self.elevator_list[2].door_open == False and self.elevator_list[2].door_state == 0:
                if self.elevator_list[2].state != -1:
                    for l in self.elevator_list[2].myList:
                        if l > self.elevator_list[2].level:
                            self.elevator_list[2].state = 1
                            self.elevator_list[2].position += 1
                            break
                    else:
                        self.elevator_list[2].state = 0
                        
                if self.elevator_list[2].state != 1:
                    for l in self.elevator_list[2].myList:
                        if l < self.elevator_list[2].level:
                            self.elevator_list[2].state = -1
                            self.elevator_list[2].position -= 1
                            break
                    else:
                        self.elevator_list[2].state = 0
            if self.elevator_list[2].door_state != 0:
                if self.elevator_list[2].state != -1 and self.elevator_list[2].level != 20:
                    eval("self.pushButton_"+ str(self.elevator_list[2].level) + "_up.setChecked(False)")
                if self.elevator_list[2].state != 1 and self.elevator_list[2].level != 1:
                    eval("self.pushButton_"+ str(self.elevator_list[2].level) + "_down.setChecked(False)")
                for l in self.elevator_list[2].myList:
                    if l > self.elevator_list[2].level:
                        pass
                else:
                    if self.elevator_list[2].level != 1:
                        eval("self.pushButton_"+ str(self.elevator_list[2].level) + "_down.setChecked(False)")
                for l in self.elevator_list[2].myList:
                    if l < self.elevator_list[2].level:
                        pass
                else:
                    if self.elevator_list[2].level != 20:
                        eval("self.pushButton_"+ str(self.elevator_list[2].level) + "_up.setChecked(False)")                

        if self.elevator_list[3].position % (5 * PIC_MOVE_INTERVAL) != 0:
            if self.elevator_list[3].state == 1:
                self.elevator_list[3].position += 1
            else:
                self.elevator_list[3].position -= 1
        else:
            if self.elevator_list[3].level in self.elevator_list[3].myList:
                self.elevator_list[3].door_open = True
                eval("self.pushButton_4_"+ str(self.elevator_list[3].level) + ".setChecked(False)")                 
                self.pushButton_4_open.setChecked(False)
                self.elevator_list[3].myList.remove(self.elevator_list[3].level)
            if self.elevator_list[3].door_open == False and self.elevator_list[3].door_state == 0:
                if self.elevator_list[3].state != -1:
                    for l in self.elevator_list[3].myList:
                        if l > self.elevator_list[3].level:
                            self.elevator_list[3].state = 1
                            self.elevator_list[3].position += 1
                            break
                    else:
                        self.elevator_list[3].state = 0
                        
                if self.elevator_list[3].state != 1:
                    for l in self.elevator_list[3].myList:
                        if l < self.elevator_list[3].level:
                            self.elevator_list[3].state = -1
                            self.elevator_list[3].position -= 1
                            break
                    else:
                        self.elevator_list[3].state = 0
            if self.elevator_list[3].door_state != 0:
                if self.elevator_list[3].state != -1 and self.elevator_list[3].level != 20:
                    eval("self.pushButton_"+ str(self.elevator_list[3].level) + "_up.setChecked(False)")
                if self.elevator_list[3].state != 1 and self.elevator_list[3].level != 1:
                    eval("self.pushButton_"+ str(self.elevator_list[3].level) + "_down.setChecked(False)")
                for l in self.elevator_list[3].myList:
                    if l > self.elevator_list[3].level:
                        pass
                else:
                    if self.elevator_list[3].level != 1:
                        eval("self.pushButton_"+ str(self.elevator_list[3].level) + "_down.setChecked(False)")
                for l in self.elevator_list[3].myList:
                    if l < self.elevator_list[3].level:
                        pass
                else:
                    if self.elevator_list[3].level != 20:
                        eval("self.pushButton_"+ str(self.elevator_list[3].level) + "_up.setChecked(False)")                

        if self.elevator_list[4].position % (5 * PIC_MOVE_INTERVAL) != 0:
            if self.elevator_list[4].state == 1:
                self.elevator_list[4].position += 1
            else:
                self.elevator_list[4].position -= 1
        else:
            if self.elevator_list[4].level in self.elevator_list[4].myList:
                self.elevator_list[4].door_open = True
                eval("self.pushButton_5_"+ str(self.elevator_list[4].level) + ".setChecked(False)")               
                self.pushButton_5_open.setChecked(False)
                self.elevator_list[4].myList.remove(self.elevator_list[4].level)
            if self.elevator_list[4].door_open == False and self.elevator_list[4].door_state == 0:
                if self.elevator_list[4].state != -1:
                    for l in self.elevator_list[4].myList:
                        if l > self.elevator_list[4].level:
                            self.elevator_list[4].state = 1
                            self.elevator_list[4].position += 1
                            break
                    else:
                        self.elevator_list[4].state = 0
                        
                if self.elevator_list[4].state != 1:
                    for l in self.elevator_list[4].myList:
                        if l < self.elevator_list[4].level:
                            self.elevator_list[4].state = -1
                            self.elevator_list[4].position -= 1
                            break
                    else:
                        self.elevator_list[4].state = 0
            if self.elevator_list[4].door_state != 0:
                if self.elevator_list[4].state != -1 and self.elevator_list[4].level != 20:
                    eval("self.pushButton_"+ str(self.elevator_list[4].level) + "_up.setChecked(False)")
                if self.elevator_list[4].state != 1 and self.elevator_list[4].level != 1:
                    eval("self.pushButton_"+ str(self.elevator_list[4].level) + "_down.setChecked(False)")
                for l in self.elevator_list[4].myList:
                    if l > self.elevator_list[4].level:
                        pass
                else:
                    if self.elevator_list[4].level != 1:
                        eval("self.pushButton_"+ str(self.elevator_list[4].level) + "_down.setChecked(False)")
                for l in self.elevator_list[4].myList:
                    if l < self.elevator_list[4].level:
                        pass
                else:
                    if self.elevator_list[4].level != 20:
                        eval("self.pushButton_"+ str(self.elevator_list[4].level) + "_up.setChecked(False)")                

    def LevelUpdate(self):
        self.elevator_list[0].level = (self.elevator_list[0].position // (5 * PIC_MOVE_INTERVAL)) + 1
        self.elevator_list[1].level = (self.elevator_list[1].position // (5 * PIC_MOVE_INTERVAL)) + 1
        self.elevator_list[2].level = (self.elevator_list[2].position // (5 * PIC_MOVE_INTERVAL)) + 1
        self.elevator_list[3].level = (self.elevator_list[3].position // (5 * PIC_MOVE_INTERVAL)) + 1
        self.elevator_list[4].level = (self.elevator_list[4].position // (5 * PIC_MOVE_INTERVAL)) + 1
        self.lcdNumber_1.setProperty("value", self.elevator_list[0].level)
        self.lcdNumber_2.setProperty("value", self.elevator_list[1].level)
        self.lcdNumber_3.setProperty("value", self.elevator_list[2].level)
        self.lcdNumber_4.setProperty("value", self.elevator_list[3].level)
        self.lcdNumber_5.setProperty("value", self.elevator_list[4].level)
    
    def UpDownUpdate(self):    
        if self.elevator_list[0].state == 1:
            self.graphicsView_1.setStyleSheet("QGraphicsView{border-image: url(" + self.MyUpPic + ")}")
        elif self.elevator_list[0].state == -1:
            self.graphicsView_1.setStyleSheet("QGraphicsView{border-image: url(" + self.MyDownPic + ")}")
        else:
            self.graphicsView_1.setStyleSheet("")
            
        if self.elevator_list[1].state == 1:
            self.graphicsView_2.setStyleSheet("QGraphicsView{border-image: url(" + self.MyUpPic + ")}")
        elif self.elevator_list[1].state == -1:
            self.graphicsView_2.setStyleSheet("QGraphicsView{border-image: url(" + self.MyDownPic + ")}")
        else:
            self.graphicsView_2.setStyleSheet("")
            
        if self.elevator_list[2].state == 1:
            self.graphicsView_3.setStyleSheet("QGraphicsView{border-image: url(" + self.MyUpPic + ")}")
        elif self.elevator_list[2].state == -1:
            self.graphicsView_3.setStyleSheet("QGraphicsView{border-image: url(" + self.MyDownPic + ")}")
        else:
            self.graphicsView_3.setStyleSheet("")
            
        if self.elevator_list[3].state == 1:
            self.graphicsView_4.setStyleSheet("QGraphicsView{border-image: url(" + self.MyUpPic + ")}")
        elif self.elevator_list[3].state == -1:
            self.graphicsView_4.setStyleSheet("QGraphicsView{border-image: url(" + self.MyDownPic + ")}")
        else:
            self.graphicsView_4.setStyleSheet("")
            
        if self.elevator_list[4].state == 1:
            self.graphicsView_5.setStyleSheet("QGraphicsView{border-image: url(" + self.MyUpPic + ")}")
        elif self.elevator_list[4].state == -1:
            self.graphicsView_5.setStyleSheet("QGraphicsView{border-image: url(" + self.MyDownPic + ")}")
        else:
            self.graphicsView_5.setStyleSheet("")
    
    def DoorUpdate(self):
        if self.elevator_list[0].door_state >= 4*PIC_CHANGE_INTERVAL:
            self.pushButton_1_open.setChecked(False)
            self.elevator_list[0].door_open = False
        if self.elevator_list[0].door_open == True:
            self.pushButton_1_open.setChecked(False) 
        if self.pushButton_1_open.isChecked():
            if self.elevator_list[0].state == 0 or self.elevator_list[0].door_state != 0:
                self.elevator_list[0].door_open = True
                self.pushButton_1_open.setChecked(False)
        if self.pushButton_1_close.isChecked():
            self.elevator_list[0].door_open = False
            self.pushButton_1_close.setChecked(False)
        if self.elevator_list[0].door_state < PIC_CHANGE_INTERVAL: 
            self.elevator_list[0].setStyleSheet("QGraphicsView{border-image: url(" + self.MyClosedPic + ")}")
        elif self.elevator_list[0].door_state < 2 * PIC_CHANGE_INTERVAL:
            self.elevator_list[0].setStyleSheet("QGraphicsView{border-image: url(" + self.MyNarrowPic + ")}")
        elif self.elevator_list[0].door_state < 3 * PIC_CHANGE_INTERVAL:
            self.elevator_list[0].setStyleSheet("QGraphicsView{border-image: url(" + self.MyWidePic + ")}")
        else:
            self.elevator_list[0].setStyleSheet("QGraphicsView{border-image: url(" + self.MyOpenPic + ")}")
        if self.elevator_list[0].door_open == True:
            if self.elevator_list[0].door_state < 4 * PIC_CHANGE_INTERVAL:
                self.elevator_list[0].door_state += 1
        else: 
            if self.elevator_list[0].door_state > 0:
                self.elevator_list[0].door_state -= 1            

        if self.elevator_list[1].door_state >= 4*PIC_CHANGE_INTERVAL:
            self.pushButton_2_open.setChecked(False)
            self.elevator_list[1].door_open = False
        if self.elevator_list[1].door_open == True:
            self.pushButton_2_open.setChecked(False) 
        if self.pushButton_2_open.isChecked():
            if self.elevator_list[1].state == 0 or self.elevator_list[1].door_state != 0:
                self.elevator_list[1].door_open = True
                self.pushButton_2_open.setChecked(False)
        if self.pushButton_2_close.isChecked():
            self.elevator_list[1].door_open = False
            self.pushButton_2_close.setChecked(False)
        if self.elevator_list[1].door_state < PIC_CHANGE_INTERVAL: 
            self.elevator_list[1].setStyleSheet("QGraphicsView{border-image: url(" + self.MyClosedPic + ")}")
        elif self.elevator_list[1].door_state < 2 * PIC_CHANGE_INTERVAL:
            self.elevator_list[1].setStyleSheet("QGraphicsView{border-image: url(" + self.MyNarrowPic + ")}")
        elif self.elevator_list[1].door_state < 3 * PIC_CHANGE_INTERVAL:
            self.elevator_list[1].setStyleSheet("QGraphicsView{border-image: url(" + self.MyWidePic + ")}")
        else:
            self.elevator_list[1].setStyleSheet("QGraphicsView{border-image: url(" + self.MyOpenPic + ")}")
        if self.elevator_list[1].door_open == True:
            if self.elevator_list[1].door_state < 4 * PIC_CHANGE_INTERVAL:
                self.elevator_list[1].door_state += 1
        else: 
            if self.elevator_list[1].door_state > 0:
                self.elevator_list[1].door_state -= 1

        if self.elevator_list[2].door_state >= 4*PIC_CHANGE_INTERVAL:
            self.pushButton_3_open.setChecked(False)
            self.elevator_list[2].door_open = False
        if self.elevator_list[2].door_open == True:
            self.pushButton_3_open.setChecked(False) 
        if self.pushButton_3_open.isChecked():
            if self.elevator_list[2].state == 0 or self.elevator_list[2].door_state != 0:
                self.elevator_list[2].door_open = True
                self.pushButton_3_open.setChecked(False)
        if self.pushButton_3_close.isChecked():
            self.elevator_list[2].door_open = False
            self.pushButton_3_close.setChecked(False)
        if self.elevator_list[2].door_state < PIC_CHANGE_INTERVAL: 
            self.elevator_list[2].setStyleSheet("QGraphicsView{border-image: url(" + self.MyClosedPic + ")}")
        elif self.elevator_list[2].door_state < 2 * PIC_CHANGE_INTERVAL:
            self.elevator_list[2].setStyleSheet("QGraphicsView{border-image: url(" + self.MyNarrowPic + ")}")
        elif self.elevator_list[2].door_state < 3 * PIC_CHANGE_INTERVAL:
            self.elevator_list[2].setStyleSheet("QGraphicsView{border-image: url(" + self.MyWidePic + ")}")
        else:
            self.elevator_list[2].setStyleSheet("QGraphicsView{border-image: url(" + self.MyOpenPic + ")}")
        if self.elevator_list[2].door_open == True:
            if self.elevator_list[2].door_state < 4 * PIC_CHANGE_INTERVAL:
                self.elevator_list[2].door_state += 1
        else: 
            if self.elevator_list[2].door_state > 0:
                self.elevator_list[2].door_state -= 1

        if self.elevator_list[3].door_state >= 4*PIC_CHANGE_INTERVAL:
            self.pushButton_4_open.setChecked(False)
            self.elevator_list[3].door_open = False
        if self.elevator_list[3].door_open == True:
            self.pushButton_4_open.setChecked(False) 
        if self.pushButton_4_open.isChecked():
            if self.elevator_list[3].state == 0 or self.elevator_list[3].door_state != 0:
                self.elevator_list[3].door_open = True
                self.pushButton_4_open.setChecked(False)
        if self.pushButton_4_close.isChecked():
            self.elevator_list[3].door_open = False
            self.pushButton_4_close.setChecked(False)
        if self.elevator_list[3].door_state < PIC_CHANGE_INTERVAL: 
            self.elevator_list[3].setStyleSheet("QGraphicsView{border-image: url(" + self.MyClosedPic + ")}")
        elif self.elevator_list[3].door_state < 2 * PIC_CHANGE_INTERVAL:
            self.elevator_list[3].setStyleSheet("QGraphicsView{border-image: url(" + self.MyNarrowPic + ")}")
        elif self.elevator_list[3].door_state < 3 * PIC_CHANGE_INTERVAL:
            self.elevator_list[3].setStyleSheet("QGraphicsView{border-image: url(" + self.MyWidePic + ")}")
        else:
            self.elevator_list[3].setStyleSheet("QGraphicsView{border-image: url(" + self.MyOpenPic + ")}")
        if self.elevator_list[3].door_open == True:
            if self.elevator_list[3].door_state < 4 * PIC_CHANGE_INTERVAL:
                self.elevator_list[3].door_state += 1
        else: 
            if self.elevator_list[3].door_state > 0:
                self.elevator_list[3].door_state -= 1

        if self.elevator_list[4].door_state >= 4*PIC_CHANGE_INTERVAL:
            self.pushButton_5_open.setChecked(False)
            self.elevator_list[4].door_open = False
        if self.elevator_list[4].door_open == True:
            self.pushButton_5_open.setChecked(False) 
        if self.pushButton_5_open.isChecked():
            if self.elevator_list[4].state == 0 or self.elevator_list[4].door_state != 0:
                self.elevator_list[4].door_open = True
                self.pushButton_5_open.setChecked(False)
        if self.pushButton_5_close.isChecked():
            self.elevator_list[4].door_open = False
            self.pushButton_5_close.setChecked(False)
        if self.elevator_list[4].door_state < PIC_CHANGE_INTERVAL: 
            self.elevator_list[4].setStyleSheet("QGraphicsView{border-image: url(" + self.MyClosedPic + ")}")
        elif self.elevator_list[4].door_state < 2 * PIC_CHANGE_INTERVAL:
            self.elevator_list[4].setStyleSheet("QGraphicsView{border-image: url(" + self.MyNarrowPic + ")}")
        elif self.elevator_list[4].door_state < 3 * PIC_CHANGE_INTERVAL:
            self.elevator_list[4].setStyleSheet("QGraphicsView{border-image: url(" + self.MyWidePic + ")}")
        else:
            self.elevator_list[4].setStyleSheet("QGraphicsView{border-image: url(" + self.MyOpenPic + ")}")
        if self.elevator_list[4].door_open == True:
            if self.elevator_list[4].door_state < 4 * PIC_CHANGE_INTERVAL:
                self.elevator_list[4].door_state += 1
        else: 
            if self.elevator_list[4].door_state > 0:
                self.elevator_list[4].door_state -= 1
    
    def PositionUpdate(self):
        pos = self.mapToGlobal(QPoint(0, 0))
        self.elevator_list[0].DecidePosition(self.pushButton_1_1, self.label_1, pos)
        self.elevator_list[1].DecidePosition(self.pushButton_2_1, self.label_21, pos)
        self.elevator_list[2].DecidePosition(self.pushButton_3_1, self.label_22, pos)
        self.elevator_list[3].DecidePosition(self.pushButton_4_1, self.label_23, pos)
        self.elevator_list[4].DecidePosition(self.pushButton_5_1, self.label_24, pos)

    def TickUpdate(self):   
        self.LevelUpdate()
        self.DispatchUpdate()
        self.ListUpdate()
        self.StateUpdate()
        self.DoorUpdate()         
        self.UpDownUpdate()
        self.PositionUpdate()
        
    def handleWarning(self):
        button = self.sender()
        if self.WarningCount >= 2:
            self.pushButton_1_warning.setEnabled(False)
            self.pushButton_2_warning.setEnabled(False)
            self.pushButton_3_warning.setEnabled(False)
            self.pushButton_4_warning.setEnabled(False)
            self.pushButton_5_warning.setEnabled(False)
            QMessageBox. critical(self, '警报','电梯维修工已经出发！') 
        if self.WarningCount == 1:
            button.setEnabled(False)
            QMessageBox. warning(self, '警报','四面回荡着警铃声…')
            self.WarningCount += 1                        
        if self.WarningCount == 0:
            button.setEnabled(False)
            QMessageBox.information(self, '警报','不寒而栗，毛骨悚然…')
            self.WarningCount += 1

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec())    
