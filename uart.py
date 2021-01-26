import serial
import queue
import threading
import datetime
import binascii


class Uart_Recv_Data_Thread(threading.Thread):
    def __init__(self, cur_self, main_self):
        super(Uart_Recv_Data_Thread, self).__init__()
        self.cur_self = cur_self
        self.thread = threading.Event()
        self.main_self = main_self

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while True:
            time = ''
            if self.stopped():
                break
            try:
                if False == self.cur_self.recv_queue.empty():
                    show_data = ''
                    data = self.cur_self.recv_queue.get()
                    data_num = len(data)
                    if self.cur_self.uart_time_stamp_flag == 1:# 时间戳开关打开
                        time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S:%f]\r\n')
                    
                    if self.cur_self.uart_rec_hex_lock == 1:
                        data_list = []
                        data_bytes = bytes(data, encoding='utf-8')
                        for i in range(len(data_bytes)):
                            data_list.append(hex(data_bytes[i])[2:].zfill(2))
                        send_text_to_hex = ' '.join(data_list)
                        show_data += send_text_to_hex
                    else:
                        show_data = data
                    
                    self.main_self.uart_recv_updata_show_data_signal.emit(time + show_data + '\r\n')

                    # 统计接收字符的数量
                    self.main_self.uart_updata_recv_num_signal.emit(data_num)

    
                nums = self.cur_self.serial.inWaiting()
                if (nums > 0):
                    recv_msg = self.cur_self.serial.read(nums)
                else:
                    continue
                if self.cur_self.recv_queue.full():
                    self.cur_self.recv_queue.get()
                self.cur_self.recv_queue.put(recv_msg.decode())

                
            except Exception as e:
                print(e)
                continue

class Uart_Send_Data_Thread(threading.Thread):
    def __init__(self, cur_self, main_self):
        super(Uart_Send_Data_Thread, self).__init__()
        self.cur_self = cur_self
        self.main_self = main_self
        self.thread = threading.Event()

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while True:
            if self.stopped():
                break
            try:
                if not self.cur_self.send_queue.empty():
                    send_data = self.cur_self.send_queue.get(False)
                    data_num = len(send_data)
                    # 统计发送字符的数量
                    self.main_self.uart_updata_send_num_signal.emit(data_num)
                    #ascii 发送
                    self.cur_self.serial.write(send_data)
                else:
                    continue
            except queue.Empty:
                continue


class Uart(object):
    def __init__(self, parent):
        self.err = 0
        self.parent = parent

        self.recv_queue = queue.Queue(1000)
        self.send_queue = queue.Queue(1000)
        self.uart_time_stamp_flag = 0
        self.uart_rec_hex_lock = 0


    def uart_init(self, port, baud, stopbit, databit, checkbit):
        try:
            checkbitlist = {'None': 'N', 'Odd': 'O', 'Even': 'E'}
            stopbitlist = {'1': 'serial.STOPBITS_ONE', '1.5': 'serial.STOPBITS_ONE', '2': 'serial.STOPBITS_ONE'}
            self.serial = serial.Serial(port.split()[0], baud, int(databit), checkbitlist[checkbit], serial.STOPBITS_ONE)
            # 创建线程
            self.recv_thread = Uart_Recv_Data_Thread(self, self.parent)
            self.send_thread = Uart_Send_Data_Thread(self, self.parent)
            self.err = 0
        except Exception as e:
            print(e)
            self.err = -1


    def open_uart_thread(self):
        self.recv_thread.start()
        self.send_thread.start()
        

    def close_uart_thread(self):
        self.recv_thread.stop()
        self.send_thread.stop()
        self.serial.close()
    
    def uart_send_func(self, data):
        self.send_queue.put(data)

    def uart_time_stamp(self, flag):
        self.uart_time_stamp_flag = flag

    def uart_set_rec_hex_lock(self, flag):
        self.uart_rec_hex_lock = flag





