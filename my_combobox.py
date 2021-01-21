import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import QComboBox


class My_ComBoBox(QComboBox):

    def __init__(self, parent = None):
        super(My_ComBoBox,self).__init__(parent)

    # 重写showPopup函数
    def showPopup(self):
        # 先清空原有的选项
        self.clear()
        index = 1

        # 获取接入的所有串口信息，插入combobox的选项中
        port_list = self.get_port_list(self)
        if port_list is not None:
            for i in port_list:
                self.insertItem(index, i)
                index += 1
        QComboBox.showPopup(self)# 弹出选项框

    @staticmethod
    # 获取接入的COM
    def get_port_list(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            for port in port_list:
                yield str(port)
        except Exception as err:
            print("获取接入的串口设备出错！错误信息为：" + str(err))