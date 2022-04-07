from flask import Flask, jsonify, render_template, request
import minimalmodbus
import time
import struct

app = Flask(__name__)

serial_device = '/dev/ttyUSB0' # RS485 device in linux

instrument = minimalmodbus.Instrument(serial_device, 1, debug = False) 

instrument.serial.baudrate = 115200
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.1          # seconds
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

def to_signed(val):
    if val > 2147483648:
        return val - 2*2147483648
    else:
        return val

def get_16l(val):
    l, h = struct.unpack('2H', struct.pack('i', val))
    return l

def get_16h(val):
    l, h = struct.unpack('2H', struct.pack('i', val))
    return h

@app.route("/")
def main():
    return render_template('main.html', reload = time.time())

@app.route("/api/info")
def api_info():
    cur_pos = to_signed(instrument.read_long(204))
    tar_pos = to_signed(instrument.read_long(198))
    cur_speed = to_signed(instrument.read_long(208))
    torque = to_signed(instrument.read_long(214))*0.1
    m_temp = instrument.read_long(250)*0.1

    info = {
       "cur_pos" : cur_pos,
       "tar_pos" : tar_pos,
       "cur_speed" : cur_speed,
       "torque" : "{:5.1f}".format(torque),
       "m_temp" : "{:5.1f}".format(m_temp)
    }
    return jsonify(info)

@app.route("/api/move")
def motor_move():
# get position (steps), default is 0
    pos = int(request.args.get('pos', 0))
# get speed (steps/s), default 1000, clamped at 5000
    speed = min(5000, int(request.args.get('speed', 1000)))
# acceleration after start (steps/s^2), default 500
    accel = int(request.args.get('accel', 500))
# deceleration before stop (steps/s^2), default 500
    decel = int(request.args.get('decel', 500))

    dd_addr = 88
    instrument.write_registers(dd_addr, [0,0,0,1,get_16h(pos),get_16l(pos),0,speed,0,accel,0,decel,0,1000,0,1])

    info = {
       "status" : "OK",
    }
    return jsonify(info)

@app.route("/api/stop")
def motor_stop():
    instrument.write_registers(124, [0,32])
    instrument.write_registers(124, [0,0])
    

    info = {
       "status" : "OK",
    }
    return jsonify(info)   

