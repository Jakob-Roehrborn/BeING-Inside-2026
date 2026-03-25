from machine import Pin, ADC
import time
import network
'''PIN_solar = Pin(16, Pin.OUT)
PIN_speicher = Pin(17, Pin.OUT)
PIN_waermepumpe = Pin(18, Pin.OUT)'''

pin_auto = Pin(15, Pin.IN, Pin.PULL_UP)
pin_solar = ADC(Pin(26))
pin_speicher = ADC(Pin(27))
pin_waermepumpe = ADC(Pin(28))

#Module = [PV,EV,WP,Batterie]




def module_check():
    modules_w=[0,0,0,0]
    if pin_solar.read_u16() > 1000:
        modules_w[0] = 1
    else: modules_w[0] = 0

    modules_w[1] = int(not pin_auto.value() )

    if pin_waermepumpe.read_u16() > 1000:
        modules_w[2] = 1
    else:
        modules_w[2] = 0
    
    if pin_speicher.read_u16() > 1000:
        modules_w[3] = 1
    else: modules_w[3] = 0
    return modules_w


def send(module,state):
    print(module,state)

def change_det(old,new):
    for i in range(4):
        if old[i] == new[i]: continue
        else: send(i, new[i])



def main():
    modules=[0,0,0,0]
    while True:
        modules_old= modules.copy()
        modules= module_check()
        change_det(modules_old,modules)
    
if __name__ == "__main__":
    main()

