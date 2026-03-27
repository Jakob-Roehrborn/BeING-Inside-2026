from machine import Pin, ADC
import network
import urequests
import ujson
import time
import errno


SSID = 'beingpico'
PASSWORD = 'bittebittegeh' 
HOST = "192.168.12.1"
PORT = "5000"

STATIC_IP = "192.168.12.5"
SUBNET_MASK = "255.255.255.0"
GATEWAY = "192.168.12.1"
DNS = "192.168.12.1"

#------------------------Logic-----------------------
#Module = [PV,EV,WP,Batterie]
pin_auto = Pin(15, Pin.IN, Pin.PULL_UP)
pin_solar = ADC(Pin(26))
pin_speicher = ADC(Pin(27))
pin_waermepumpe = ADC(Pin(28))

Pin(16, Pin.OUT).value(1)
Pin(17, Pin.OUT).value(1)
Pin(18, Pin.OUT).value(1)

empty_list = [0 for i in range(512)]
modules_w=[empty_list.copy() for i in range(4)]
def module_check(i):
    
    if pin_solar.read_u16() > 1000:
        modules_w[0][i] = 1
    else: modules_w[0][i] = 0

    modules_w[1][i] = int(not pin_auto.value() )

    if pin_waermepumpe.read_u16() > 1000:
        modules_w[2][i] = 1
    else:
        modules_w[2][i] = 0
    
    if pin_speicher.read_u16() > 1000:
        modules_w[3][i] = 1
    else: modules_w[3][i] = 0
    return modules_w


    

def send(module: int, state: int):
    payload = {
        "module" : module,
        "state": state,
    }
    headers = {"Content-Type": "application/json"}
    json_data = ujson.dumps(payload)
    print(payload)
    try: 
        response = urequests.post(f'http://{HOST}:{PORT}/api/module_change', data=json_data, headers=headers)
        print(response)
        response.close()

    except OSError as e :
        if e.errno == errno.EHOSTUNREACH:
                print(f"Error: Host unreachable for index")
        print(e)
    


av=[0,0,0,0]

def change_det(new, old_av):
    for k in range(4):
        av[k] = round(sum(new[k]) / len(new[k]))
        if av[k] == old_av[k]: continue
        send(k, av[k])

#-------------------------Network-----------------------------

def network_init():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY, DNS))
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("connecting")
        time.sleep(1)
    print("con successfull")

#--------------------------Main-------------------------------

def main():
    modules=[[0],[0],[0],[0]]
    network_init()
    send(6,6)
    i = 0
    while True:
        modules= module_check(i)
        old_average = av.copy()
        change_det(modules, old_average)
        i+=1
        i = i%512
    
if __name__ == "__main__":
    main()

