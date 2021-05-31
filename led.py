# coding=utf-8

import mraa
from time import sleep

class LED:
    def __init__(self):
        '''
        LED的初始化：定义GPIO为输出，并全部写0，关闭LED
        '''
        self.r = mraa.Gpio(2)
        self.g = mraa.Gpio(3)
        self.b = mraa.Gpio(4)       
        self.r.dir(mraa.DIR_OUT)
        self.g.dir(mraa.DIR_OUT)
        self.b.dir(mraa.DIR_OUT)
        self.r.write(0)
        self.g.write(0)
        self.b.write(0)
        self.rgb = zip(['r','g','b'],[self.r,self.g,self.b])

    def open(self, idx):
        '''
        通过向GPIO写1，打开特定的灯光
        '''
        try:
            self.rgb[idx].write(1)
        except:
            print("wrong idx, open failed")

    def close(self, idx):
        '''
        通过向GPIO写0，关闭特定的灯光
        '''
        try:
            self.rgb[idx].write(0)
        except:
            print("wrong idx, open failed")

    def show(self):
        lists = ['r','g','b']
        idx=0
        while 1:
            self.open(lists[idx%3])
            sleep(1)
            self.close(lists[idx%3])
            sleep(1)
            idx += 1


def led_init():
    r = mraa.Gpio(2)
    g = mraa.Gpio(3)
    b = mraa.Gpio(4)

 if __name__ == '__main__':
    led = LED()
    led.show()
    print("Type any key to exit...")
    raw_input()
    led.close('r')
    led.close('g')
    led.close('b')
    print("Exit")
