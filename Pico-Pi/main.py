from machine import Pin, ADC
import network
import urequests
import time


#------------------------Logic-----------------------
#Module = [PV,EV,WP,Batterie]
pin_auto = Pin(15, Pin.IN, Pin.PULL_UP)
pin_solar = ADC(Pin(26))
pin_speicher = ADC(Pin(27))
pin_waermepumpe = ADC(Pin(28))

Pin(16, Pin.OUT).value(1)
Pin(17, Pin.OUT).value(1)
Pin(18, Pin.OUT).value(1)

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
    message = (module,state)
    response = urequests.post('http://127.0.0.1:5000/module_change', data = {message})
    print(response)


def change_det(old,new):
    for i in range(4):
        if old[i] == new[i]: continue
        send(i, new[i])
        time.sleep(0.5)

#-------------------------Network-----------------------------
ssid = 'vindictiveVi'
password = 'getonthisshit' 
def network_init():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
            print("connecting")
            time.sleep(0.1)
    print("con successfull")

#--------------------------Main-------------------------------

def main():
    modules=[0,0,0,0]
    network_init()
    message=(1,2)
    response = urequests.post('http://127.0.0.1:5000/module_change', data = {message})
    print(response)
    while True:
        modules_old= modules.copy()
        modules= module_check()
        change_det(modules_old,modules)
    
if __name__ == "__main__":
    main()

