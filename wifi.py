

import ujson as json
import network

def do_connect():
        config_file = 'config.json'
        with open(config_file) as f:
                config = json.load(f)               
        sta_if = network.WLAN(network.STA_IF)
        # Activate AP interface for manage
        ap_if = network.WLAN(network.AP_IF)
        if not sta_if.isconnected():
                print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config["ESSID"], config["PASSWORD"])
        while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())
        # Disable AP 
        ap_if.active(False) 