


import ujson as json
import machine
import time

"""   Загружаем конфиг   """
config_file = 'config.json'
with open(config_file) as f:
  config = json.load(f)

"""    Определяем выводы для реле   """
relay1 = machine.Pin(int(config["relay_1_pin"]), machine.Pin.OUT)
# relay2 = machine.Pin(config["relay_2_pin"], machine.Pin.OUT)
# relay3 = machine.Pin(config["relay_3_pin"], machine.Pin.OUT)
# relay4 = machine.Pin(config["relay_4_pin"], machine.Pin.OUT)

def save_config():
    config_file = 'config.json'
    with open(config_file, 'w') as f:
        config = json.dump(f)

""" Relay function """
def relay_on(relay):
    relay.off()
    
def relay_off(relay):
    relay.on()

def automatic_relay_control(relay, start_time, stop_time):
    # get current time
    current_time = list(time.localtime())
    print("True time", current_time) # remove after debug
    #apply time zone
    current_time[3] += int(config["time_zone"])
    # create list, start/stop, time for compare
    r_start_time = current_time[:]
    r_start_time[3:5] = int(start_time[0]), int(start_time[1])
    r_stop_time = current_time[:]
    r_stop_time[3:5] = int(stop_time[0]), int(stop_time[1])
   
    #x < y < z.
    if ((tuple(current_time) >= tuple(r_start_time)) and (tuple(current_time) <= tuple(r_stop_time))):
        relay_on(relay)
        print("Relay ON", current_time)
    else:
        relay_off(relay)
        print("Relay OFF", current_time)
    time.sleep(2)

""" Thermo test """

""" PH test """

# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

def web_page():
  if relay1.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  automatic_relay_control(relay1, config["light_relay_start"], config["light_relay_stop"])
  # automatic_relay_control(relay2, st.filter_relay_start, st.filter_relay_stop)
  # automatic_relay_control(relay3, st.compressor_relay_start, st.compressor_relay_stop)

  # conn, addr = s.accept()
  # print('Got a connection from %s' % str(addr))
  # request = conn.recv(1024)
  # request = str(request)
  # print('Content = %s' % request)
  # led_on = request.find('/?led=on')
  # led_off = request.find('/?led=off')
  # if led_on == 6:
  #   print('LED ON')
  #   relay1.value(1)
  # if led_off == 6:
  #   print('LED OFF')
  #   relay1.value(0)
  # response = web_page()
  # conn.send('HTTP/1.1 200 OK\n')
  # conn.send('Content-Type: text/html\n')
  # conn.send('Connection: close\n\n')
  # conn.sendall(response)
  # conn.close()