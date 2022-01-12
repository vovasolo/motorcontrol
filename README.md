# motorcontrol

A Flask application providing a minimal web interface to Oriental Motor AZD step motor controller. 

Using MODBUS over RS485. Set the correct `serial_device` in the `app.py` before running.

Installing dependences:
```
pip install flask minimalmodbus
```  

To run the application, cd to the directory where `app.py` is and execute `flask run` command from there. Then open http://localhost:5000 in the browser and enjoy

Run with `flask run -p XXXX` to listen on port XXXX instead of default 5000
