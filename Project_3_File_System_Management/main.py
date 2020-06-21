import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore

# 导入UI文件
import FileSystem


# 加载图片资源文件
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 界面主线程
class MyWindow(QMainWindow, FileSystem.Ui_MainWindow):
    # 对界面进行初始化
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        # 设置图标
        MyICO = resource_path(os.path.join("res","favicon.ico"))
        self.setWindowIcon(QIcon(MyICO))
        # 增加各按钮的回调函数
        self.NewFileButton.clicked.connect(self.NewFile)
        self.NewDirectoryButton.clicked.connect(self.NewDirectory)
        self.SaveAndExitButton.clicked.connect(self.SaveAndExit)
        self.FormatButton.clicked.connect(self.Format)
        self.SaveButton.clicked.connect(self.Save)
        self.ReturnToParentButton.clicked.connect(self.ReturnToParent)
        self.CancelButton.clicked.connect(self.Cancel)
        # 设置右键菜单
        self.FileListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.FileListWidget.customContextMenuRequested.connect(self.ShowMenu)
        # 当前右键点击的文件
        self.CurrentFile = None
        # 当前所处的目录名
        self.CurrentWorkingDirectory = ""
        # 当前路径
        self.CurrentWorkingPath = "当前目录：/"
        # 当前路径（列表形式）
        self.CurrentPathList = [""]
        # 保存在内存的 32MB 字节串
        self.InnerDataBase = []
        # 当前目录中包含的文件（文件名，初始块地址，文件大小，文件类型；"Parent\n"是返回上级目录）
        self.CurrentDirectoryList = [["Parent\n"], [0], [0], [1]]
        # 当前目录的初始块地址，根目录的初始块地址是4
        self.CurrentDirectoryNode = 4
        # 当前编辑的文本文档的初始块地址
        self.CurrentEditingTextNode = 0
        # 初始化右键菜单
        self.InitMenu()
        # 初始化文件系统
        self.InitFileSystem()
 
    def InitFileSystem(self):
        myDataPath = "./FileSystem.mimg"
        # 如果不存在文件，就初始化该文件
        if not os.path.exists(myDataPath):
            # 初始化位图，b"\xf8"代表前5块（0-3块是位图，第4块是根目录初始块）已经被占用
            self.InnerDataBase.append(b"\xf8" + b"\x00" * 1023)
            for counter in range(1024 * 32 - 1):
                self.InnerDataBase.append(b"\x00" * 1024)
            # 初始化根目录
            packed_bytes = self.PackDirectory([["Parent\n"], [0], [0], [1]])
            self.CurrentDirectoryList = [["Parent\n"], [0], [0], [1]]
            self.WriteFile(4, packed_bytes)
            return None
        # 读入文件
        myData = open(myDataPath, "rb")
        for counter in range(1024 * 32):
            tmp_bytes = myData.read(1024)
            self.InnerDataBase.append(tmp_bytes)
        myData.close()
        packed_bytes = self.ReadFile(4)
        self.CurrentDirectoryList = self.UnpackDirectory(packed_bytes)
        for i in range(1, len(self.CurrentDirectoryList[0])):
            item = ""
            if self.CurrentDirectoryList[3][i] == 0:
                item = "文本文件" + "\t\t" + self.CurrentDirectoryList[0][i]
            else:
                item = "目录文件" + "\t\t" + self.CurrentDirectoryList[0][i]
            self.FileListWidget.addItem(item)
    
    # 新建文本文件，b"\xfe\xfe"是EOF
    def NewFile(self, event):
        defaultFileCounter = 1
        while True:
            default_str = "新建文本文件" + str(defaultFileCounter) + ".txt"
            count = self.FileListWidget.count()
            for i in range(count):
                if self.FileListWidget.item(i).text() == "文本文件" + "\t\t" + default_str:
                    defaultFileCounter += 1
                    break
            else:
                break
        value, ok = QInputDialog.getText(self, "新建文件", "请输入文件名:", QLineEdit.Normal, default_str)
        if ok == False:
            return None
        if str(value) == "":
            QMessageBox. warning(self, '新建失败','文件名不能为空。')
            return None          
        item = "文本文件" + "\t\t" + str(value)
        count = self.FileListWidget.count()
        for i in range(count):
            if self.FileListWidget.item(i).text() == item:
                QMessageBox. warning(self, '新建失败','同目录下不能有同名文件。')
                return None
        else:
            self.FileListWidget.addItem(item)
            self.CurrentDirectoryList[0].append(value)
            tmp_value = self.AssignMemory()
            self.CurrentDirectoryList[1].append(tmp_value)
            self.CurrentDirectoryList[2].append(0)
            self.CurrentDirectoryList[3].append(0)
            self.WriteFile(tmp_value, b"\xfe\xfe")            
            
    # 新建目录文件    
    def NewDirectory(self, event):
        defaultDirectoryCounter = 1
        while True:
            default_str = "新建文件夹" + str(defaultDirectoryCounter)
            count = self.FileListWidget.count()
            for i in range(count):
                if self.FileListWidget.item(i).text() == "目录文件" + "\t\t" + default_str:
                    defaultDirectoryCounter += 1
                    break
            else:
                break    
        value, ok = QInputDialog.getText(self, "新建目录", "请输入目录名:", QLineEdit.Normal, default_str)
        if ok == False:
            return None
        if str(value) == "":
            QMessageBox. warning(self, '新建失败','目录名不能为空。')
            return None               
        item = "目录文件" + "\t\t" + str(value)
        count = self.FileListWidget.count()
        for i in range(count):
            if self.FileListWidget.item(i).text() == item:
                QMessageBox. warning(self, '新建失败','同目录下不能有同名文件夹。')
                return None
        else:
            self.FileListWidget.addItem(item)
            self.CurrentDirectoryList[0].append(value)
            tmp_value = self.AssignMemory()
            self.CurrentDirectoryList[1].append(tmp_value)
            self.CurrentDirectoryList[2].append(0)
            self.CurrentDirectoryList[3].append(1)
            packed_bytes = self.PackDirectory([["Parent\n"], [self.CurrentDirectoryNode], [0], [1]])
            self.WriteFile(tmp_value, packed_bytes)
    
    # 格式化，基本就是把不存在.mimg时的初始化操作重做了一遍
    def Format(self):
        reply = QMessageBox.question(self,
                      "格式化", 
                      "确认要删除所有文件吗？", 
                      QMessageBox.Yes | QMessageBox.No)
        if(reply == QMessageBox.Yes):   
            self.FileListWidget.clear()
            self.SaveButton.setEnabled(False)
            self.CancelButton.setEnabled(False)
            self.PlainTextEdit.clear()
            self.PlainTextEdit.setEnabled(False)
            self.CurrentWorkingDirectory = ""
            self.CurrentWorkingPath = "当前目录：/"
            self.CurrentPathList = [""]
            self.InnerDataBase = []
            self.CurrentPathLabel.setText(self.CurrentWorkingPath)
            self.CurrentFile = None
            self.CurrentEditingTextNode = 0 
            self.InnerDataBase.append(b"\xf8" + b"\x00" * 1023)
            for counter in range(1024 * 32 - 1):
                self.InnerDataBase.append(b"\x00" * 1024) 
            packed_bytes = self.PackDirectory([["Parent\n"], [0], [0],[1]])
            self.CurrentDirectoryList = [["Parent\n"], [0], [0],[1]]
            self.WriteFile(4, packed_bytes)
            self.CurrentDirectoryNode = 4
    
    # 初始化右键菜单
    def InitMenu(self):
        self.popMenu = QMenu(self)
        openFileAction = QAction('打开', self)
        renameFileAction = QAction('重命名', self)
        deleteFileAction = QAction('删除', self)
        openFileAction.triggered.connect(self.openFileAction)
        renameFileAction.triggered.connect(self.renameFileAction)
        deleteFileAction.triggered.connect(self.deleteFileAction)
        self.popMenu.addAction(openFileAction)
        self.popMenu.addAction(renameFileAction)
        self.popMenu.addAction(deleteFileAction)       
    
    # 显示右键菜单
    def ShowMenu(self, pos):
        source = self.sender()
        # 确定被点击的是列表中的哪一项
        item = source.itemAt(pos)
        if item != None:
            self.CurrentFile = item
            self.popMenu.exec_(source.mapToGlobal(pos))
    
    # 直接点叉时提示用户是否要保存
    def closeEvent(self, QCloseEvent): 
        reply = QMessageBox.warning(self,
                      "不保存退出", 
                      "确认要放弃所有更改直接退出吗？\n“保存”只是将数据写进内存，“保存并退出系统”可以保存更改到磁盘并退出程序。", 
                      QMessageBox.Yes | QMessageBox.No)
        if(reply == QMessageBox.Yes):
            QCloseEvent.accept()
        if(reply==QMessageBox.No):
            QCloseEvent.ignore()
     
    # 正常的保存并退出
    def SaveAndExit(self, event):
        if self.SaveButton.isEnabled():
            self.Save()
        packed_bytes = self.PackDirectory(self.CurrentDirectoryList)
        self.CutToZeroFile(self.CurrentDirectoryNode)
        self.WriteFile(self.CurrentDirectoryNode, packed_bytes)
        myDataPath = "./FileSystem.mimg"
        myData = open(myDataPath, "wb")
        for counter in self.InnerDataBase:
            myData.write(counter)
        myData.close()
        QApplication.quit()
    
    # 重命名文本/目录文件
    def renameFileAction(self):
        row = self.FileListWidget.row(self.CurrentFile)
        FormerStr = self.CurrentFile.text()
        str_part1 = FormerStr[:len("**文件\t\t")]
        str_part2 = FormerStr[len("**文件\t\t"):]
        value, ok = QInputDialog.getText(self, "重命名", "请输入文件/目录名:", QLineEdit.Normal, str_part2)
        if ok == False:
            return None 
        if str(value) == "":
            QMessageBox. warning(self, '重命名失败','文件/目录名不能为空。')
            return None           
        item = str_part1 + str(value)
        count = self.FileListWidget.count()
        for i in range(count):
            if self.FileListWidget.item(i).text() == item:
                QMessageBox. warning(self, '重命名失败','同目录下不能有同名文件/目录。')
                return None
        else:            
            self.FileListWidget.takeItem(row)
            self.FileListWidget.insertItem(row, item)
            self.CurrentDirectoryList[0][self.CurrentDirectoryList[0].index(str_part2)] = value
            self.CutToZeroFile(self.CurrentDirectoryNode)
            self.WriteFile(self.CurrentDirectoryNode, self.PackDirectory(self.CurrentDirectoryList))            
    
    # 删除文本/目录文件
    def deleteFileAction(self):
        row = self.FileListWidget.row(self.CurrentFile)
        FormerStr = self.CurrentFile.text()
        str_part1 = FormerStr[:len("**")]
        str_part2 = FormerStr[len("**文件\t\t"):]
        if str_part1 == "文本":
            self.CutToZeroFile(self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)])
            self.EraseData(self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)])
        else:
            self.removeDirectory(self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)])
        del self.CurrentDirectoryList[3][self.CurrentDirectoryList[0].index(str_part2)]
        del self.CurrentDirectoryList[2][self.CurrentDirectoryList[0].index(str_part2)]
        del self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)]
        del self.CurrentDirectoryList[0][self.CurrentDirectoryList[0].index(str_part2)]
        self.FileListWidget.takeItem(row)
    
    # 删除目录需要递归删除，所以专门拉出来当个函数
    def removeDirectory(self, node):
        tmpDirectoryList = self.UnpackDirectory(self.ReadFile(node))
        for i in range(1, len(tmpDirectoryList[0])):
            if tmpDirectoryList[3][i] == 1:
                self.removeDirectory(tmpDirectoryList[1][i])
                self.CutToZeroFile(tmpDirectoryList[1][i])
                self.EraseData(tmpDirectoryList[1][i])
            else:
                self.CutToZeroFile(tmpDirectoryList[1][i])
                self.EraseData(tmpDirectoryList[1][i])                
    
    # 打开文件
    def openFileAction(self):
        FormerStr = self.CurrentFile.text()
        str_part1 = FormerStr[:len("**")]
        str_part2 = FormerStr[len("**文件\t\t"):]
        # 打开目录文件时先保存当前目录的更改，再切换到新目录
        if str_part1 == "目录":
            self.CurrentWorkingDirectory = str_part2
            # 路径太长时候换行显示
            former_length = len(self.CurrentWorkingPath) % 30
            self.CurrentWorkingPath += self.CurrentWorkingDirectory
            current_length = len(self.CurrentWorkingPath) % 30
            if current_length - former_length <= 0 or former_length == 0:
                self.CurrentWorkingPath += "\n/"
            else:
               self.CurrentWorkingPath += "/" 
            self.CurrentPathLabel.setText(self.CurrentWorkingPath)
            self.FileListWidget.clear()
            self.CurrentPathList.append(str_part2)
            self.ReturnToParentButton.setEnabled(True)
            self.CutToZeroFile(self.CurrentDirectoryNode)
            self.WriteFile(self.CurrentDirectoryNode, self.PackDirectory(self.CurrentDirectoryList))
            self.CurrentDirectoryNode = self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)]
            self.CurrentDirectoryList = self.UnpackDirectory(self.ReadFile(self.CurrentDirectoryNode))
            for i in range(1, len(self.CurrentDirectoryList[0])):
                item = ""
                if self.CurrentDirectoryList[3][i] == 0:
                    item = "文本文件" + "\t\t" + self.CurrentDirectoryList[0][i]
                else:
                    item = "目录文件" + "\t\t" + self.CurrentDirectoryList[0][i]
                self.FileListWidget.addItem(item)            
        else:
            self.SaveButton.setEnabled(True)
            self.CancelButton.setEnabled(True)
            self.PlainTextEdit.setEnabled(True)
            self.FileListWidget.setEnabled(False)
            self.ReturnToParentButton.setEnabled(False)
            self.NewFileButton.setEnabled(False)
            self.NewDirectoryButton.setEnabled(False)
            self.FormatButton.setEnabled(False)
            self.CurrentEditingTextNode = self.CurrentDirectoryList[1][self.CurrentDirectoryList[0].index(str_part2)]
            self.TextSize.setText("文本文件大小（打开文件时）：" + str(self.CurrentDirectoryList[2][self.CurrentDirectoryList[1].index(self.CurrentEditingTextNode)]) + " B")
            PlainText = str(self.ReadFile(self.CurrentEditingTextNode), encoding="utf-8")
            self.PlainTextEdit.setPlainText(PlainText)
     
    # 保存文本文件，实际上是把文件截短到零再重新写入
    def Save(self):
        PlainText = self.PlainTextEdit.toPlainText()
        self.SaveButton.setEnabled(False)
        self.CancelButton.setEnabled(False)
        self.PlainTextEdit.clear()
        self.PlainTextEdit.setEnabled(False)
        packed_text = PlainText.encode(encoding = 'utf-8')
        length = len(packed_text) // 1022 + 1
        if length % 1022 == 1021:
            packed_text = packed_text + b'\xfe'
        elif length % 1022 != 0:
            packed_text = packed_text + b'\xfe\xfe'        
        self.CutToZeroFile(self.CurrentEditingTextNode)
        self.WriteFile(self.CurrentEditingTextNode, packed_text)
        self.CurrentDirectoryList[2][self.CurrentDirectoryList[1].index(self.CurrentEditingTextNode)] = len(packed_text)
        if self.CurrentWorkingDirectory != "":
            self.ReturnToParentButton.setEnabled(True)
        self.FileListWidget.setEnabled(True)
        self.NewFileButton.setEnabled(True)
        self.NewDirectoryButton.setEnabled(True)
        self.FormatButton.setEnabled(True)
        self.TextSize.setText("文本文件大小（打开文件时）：")
    
    # 放弃更改
    def Cancel(self):
        self.SaveButton.setEnabled(False)
        self.CancelButton.setEnabled(False)
        self.PlainTextEdit.clear()
        self.PlainTextEdit.setEnabled(False)
        if self.CurrentWorkingDirectory != "":
            self.ReturnToParentButton.setEnabled(True)
        self.FileListWidget.setEnabled(True)
        self.NewFileButton.setEnabled(True)
        self.NewDirectoryButton.setEnabled(True)
        self.FormatButton.setEnabled(True)
        self.TextSize.setText("文本文件大小（打开文件时）：")        
    
    # 返回上级目录，这也需要保存当前目录
    def ReturnToParent(self):
        if self.CurrentWorkingPath[-2] == "\n":
            self.CurrentWorkingPath = self.CurrentWorkingPath[:-(len(self.CurrentWorkingDirectory) + 1 + 1)]
        else:
            self.CurrentWorkingPath = self.CurrentWorkingPath[:-(len(self.CurrentWorkingDirectory) + 1)] 
        self.CurrentPathLabel.setText(self.CurrentWorkingPath)
        self.FileListWidget.clear()
        self.CurrentPathList.pop()
        self.CurrentWorkingDirectory = self.CurrentPathList[-1]
        if self.CurrentWorkingDirectory == "":
            self.ReturnToParentButton.setEnabled(False)
        self.CutToZeroFile(self.CurrentDirectoryNode)
        self.WriteFile(self.CurrentDirectoryNode, self.PackDirectory(self.CurrentDirectoryList))
        self.CurrentDirectoryNode = self.CurrentDirectoryList[1][0]
        self.CurrentDirectoryList = self.UnpackDirectory(self.ReadFile(self.CurrentDirectoryNode))
        for i in range(1, len(self.CurrentDirectoryList[0])):
            item = ""
            if self.CurrentDirectoryList[3][i] == 0:
                item = "文本文件" + "\t\t" + self.CurrentDirectoryList[0][i]
            else:
                item = "目录文件" + "\t\t" + self.CurrentDirectoryList[0][i]
            self.FileListWidget.addItem(item)
    
    # 每个块的最后两个字节用来保存文件后继块（如果有）的地址，这个函数将两个字节的地址转换成整数
    def locate(self, word):
        location = int.from_bytes(word, byteorder='big')
        return location
    
    # 分配块，这里倒来倒去只是为了将被分配出去的一块在位图中的对应位置1
    def AssignMemory(self):
        location = 0
        for i in range(4):
            my_tmp_array = bytearray(self.InnerDataBase[i])
            for j in range(1024):
                if my_tmp_array[j] != 255:
                    tmp_str_list = bin(my_tmp_array[j])[2:]
                    while len(tmp_str_list) < 8:
                        tmp_str_list = '0' + tmp_str_list
                    tmp_str_list = list(tmp_str_list)
                    for k in range(8):
                        if tmp_str_list[k] == '0':
                            tmp_str_list[k] = '1'
                            location = i * 1024 * 8 + j * 8 + k
                            break
                    my_tmp_array[j] = int("".join(tmp_str_list), 2)
                    self.InnerDataBase[i] = bytes(my_tmp_array)
                    return location
        QMessageBox. critical(self, '错误','没有空余空间！\n程序将自动退出，所有更改将被抛弃。') 
        QApplication.quit()
    
    # 向一块中写入数据
    def AddData(self, location, data, next):
        next = next.to_bytes(2, byteorder='big')
        my_tmp_array = bytearray(self.InnerDataBase[location])
        for i in range(1022):
            if i < len(data):
                my_tmp_array[i] = data[i]
            else:
                my_tmp_array[i] = 0       
        my_tmp_array[1022] = next[0]
        my_tmp_array[1023] = next[1]
        self.InnerDataBase[location] = bytes(my_tmp_array)
    
    # 清除一个块中的数据，并将位图中的相应位置0
    def EraseData(self, location):
        my_tmp_array = bytearray(self.InnerDataBase[location])
        for i in range(1024):
            my_tmp_array[i] = 0
        self.InnerDataBase[location] = bytes(my_tmp_array)
        i = location // (1024 * 8)
        j = (location - i * 1024 * 8) // 8
        k = location % 8
        my_tmp_array = bytearray(self.InnerDataBase[i])
        tmp_str_list = bin(my_tmp_array[j])[2:]
        while len(tmp_str_list) < 8:
            tmp_str_list = '0' + tmp_str_list
        tmp_str_list = list(tmp_str_list)
        tmp_str_list[k] = '0'
        my_tmp_array[j] = int("".join(tmp_str_list), 2)
        self.InnerDataBase[i] = bytes(my_tmp_array)
    
    # 把目录从列表打包成字节串
    def PackDirectory(self, my_list):
        packed_bytes = b''
        str_list, location_list, size_list, type_list = my_list
        for i in range(len(str_list)):
            packed_bytes += str_list[i].encode(encoding = 'utf-8') + b'\xff' + location_list[i].to_bytes(2, byteorder='big') + size_list[i].to_bytes(2, byteorder='big')  + \
            type_list[i].to_bytes(2, byteorder='big') + b'\xff'
        return packed_bytes
    
    # 把目录从字节串还原成列表
    def UnpackDirectory(self, packed_bytes):
        i = 0
        str_list = []
        location_list = []
        size_list = []
        type_list = []
        while(i < len(packed_bytes)):
            while(packed_bytes[i] != 255):
                i += 1
            str_list.append(packed_bytes[0:i].decode(encoding = 'utf-8'))
            location_list.append(int.from_bytes(packed_bytes[i + 1:i + 3], byteorder='big'))
            size_list.append(int.from_bytes(packed_bytes[i + 3:i + 5], byteorder='big'))
            type_list.append(int.from_bytes(packed_bytes[i + 5:i + 7], byteorder='big'))
            packed_bytes = packed_bytes[i + 8:]
            i = 0
        return [str_list, location_list, size_list, type_list]
    
    # 读取文件，254对应b"\xfe"，连续两个254就是EOF
    def ReadFile(self, start_location):
        file_bytes = b''
        tmp_location = start_location
        while tmp_location != 0:
            if self.locate(self.InnerDataBase[tmp_location][1022:]) != 0:
                file_bytes += self.InnerDataBase[tmp_location][:1022]
            else:
                i = -1
                while i < 1022:
                    i += 1
                    if self.InnerDataBase[tmp_location][i] == 254 and self.InnerDataBase[tmp_location][i + 1] == 254:
                        break
                file_bytes += self.InnerDataBase[tmp_location][:i]
            tmp_location = self.locate(self.InnerDataBase[tmp_location][1022:])
        return file_bytes
    
    # 截短到0，由于写入时候是整块写入，所以这里实际上并没有清除初始块中的数据
    def CutToZeroFile(self, start_location):
        block_list = []
        tmp_location = start_location
        while tmp_location != 0:
            block_list.append(tmp_location)
            tmp_location = self.locate(self.InnerDataBase[tmp_location][1022:])
        release_or_not = False
        for i in block_list:
            if release_or_not == True:
                self.EraseData(i)
            else:
                release_or_not = True
    
    # 写入文件
    def WriteFile(self, start_location, packed_data):
        length = len(packed_data) // 1022 + 1
        if length % 1022 == 1021:
            packed_data = packed_data + b'\xfe'
        elif length % 1022 != 0:
            packed_data = packed_data + b'\xfe\xfe'
        while(length > 0):
            length -= 1
            if length == 0:
                self.AddData(start_location, packed_data[:1022], 0)
            else:
                tmp_location = self.AssignMemory()
                self.AddData(start_location, packed_data[:1022], tmp_location)
                start_location = tmp_location
            packed_data = packed_data[1022:]

            
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec())    
