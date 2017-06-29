import cm
import utime
import network
import ubinascii
import machine
import socket

led = cm.LED(2)

led.on()

fin = cm.Servo("D7")
pitch = cm.Servo("D8")
#pitch.middle()

led.blink(1)

credentials = cm.get_attributes('credentials.txt')

print(credentials)

print('starting network ...')

credentials = cm.get_attributes('credentials.txt')

print(credentials)

#ap_if = network.WLAN(network.AP_IF)
#print(ap_if.active())
#print(ap_if.ifconfig())

led.blink(2)

net = cm.connect()

led.blink(5)

html = """<!DOCTYPE html>
<html>
<head> 
   <title>ESP8266 Fish</title> 
</head>
<body>
<center>
<h3>Cloudmesh.robot</h3>
<h2>ESP8266 Fish</h2>
</center>
<form>
<center>
<button name="LEFT" value="ON" type="submit">LEFT</button></br>
<button name="RIGHT" value="ON" type="submit">RIGHT</button></br>
<button name="MIDDLE" value="ON" type="submit">MIDDLE</button></br>
<button name="STOP" value="ON" type="submit">STOP</button></br>
<button name="FORWARD" value="ON" type="submit">FORWARD</button></br>
<button name="UP" value="ON" type="submit" >UP</button></br>
<button name="MIDDLE" value="ON" type="submit" >MIDDLE</button></br>
<button name="DOWN" value="ON" type="submit">DOWN</button></br>
<button name="END" value="ON" type="submit">END</button></br>
</center>
</form>
</body>
</html>
"""

#p = pitch()

# Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
terminate = False

pitch.mean()
pitch.off()
position = pitch.middle()

while not terminate:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)

    LEFTON = request.find('/?LEFT=ON')
    RIGHTON = request.find('/?RIGHT=ON')
    MIDDLEON = request.find('/?MIDDLE=ON')
    FORWARD = request.find('/?FORWARD=ON')
    STOP = request.find('/?STOP=ON')
    UP = request.find('/?UP=ON')
    MIDDLE = request.find('/?MIDDLE=ON')
    DOWN = request.find('/?DOWN=ON')
    END = request.find('/?END=ON')

    direction = 'STOP'
    left_on = False
    right_on = False
    dt = 0.4
    if END == 6:
        terminate = True
        break;
    elif LEFTON == 6:
        fin.low()
        utime.sleep(dt)
        fin.off()
    elif RIGHTON == 6:
        fin.high()
        utime.sleep(dt)
        fin.off()
    elif MIDDLEON == 6:
        fin.mean()
        utime.sleep(dt)
        fin.off()
    elif STOP == 6:
        fin.off()
        utime.sleep(dt)
        fin.off()
    elif FORWARD == 6:
        fin.swim(1, 0.5)
        fin.off()
    elif UP == 6:
        pass
        #if position < pitch.maximum:
        #    position = position + 10
        #    pitch.set(position, dt=0.3)
    elif DOWN == 6:
        pass
        #if position > pitch.minimim:
        #    position = position - 10
        #    pitch.set(position, dt=0.3)
    elif MIDDLE == 6:
        pitch.mean()
        pitch.off()



    cm.feedback(conn, html)

    conn.close()