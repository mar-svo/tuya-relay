"""
<plugin key="tuya-relay" name="TUYA Relay" author="Maxim" version="2023.01">
    <description>
        <h3>TUYA Relays</h3>
        <p>Use: <a href="https://pypi.org/project/tinytuya/#description">PyPI: TinyTuya</a></p>
	<p>Local ID gets via cmd: <pre>python3 -m tinytuya wizard</pre></p>
	<p>Tuya IDs: <a href="https://eu.iot.tuya.com/cloud/basic">https://eu.iot.tuya.com/cloud/basic</a></p>
    </description>
    <params>
        <param field="SerialPort" label="Type" width="140px" required="true">
            <options>
                <option label="1-relay" value="1"/>
                <option label="2-relay" value="2"/>
                <option label="4-relay" value="4"/>
            </options>
        </param>
        <param field="Address" label="TCP IPv4 Address" width="140px" default="172.16.0.000"/>
        <param field="Username" label="Device ID" width="140px" default=""/>
        <param field="Password" label="Local Key" width="140px" default=""/>
    </params>
</plugin>
"""

import Domoticz
import tinytuya

class TuyaRelay:

    def __init__(self):
        return

    def onStart(self):
        Domoticz.Heartbeat(10)
        
        for i in range(1, int(Parameters["SerialPort"]) + 1):
            if i not in Devices: Domoticz.Device(Unit = i, DeviceID = "relay" + str(i), Name = "Relay " + str(i), Type=244, Subtype=73, Switchtype=0, Used=1).Create()
        return

    def onCommand(self, Unit, Command, Level, Hue):
        
        d = tinytuya.OutletDevice(Parameters["Username"], Parameters["Address"], Parameters["Password"])
        d.set_version(3.3)
                
        if Command == "On":
            d.turn_on(Unit)

        if Command == "Off":
            d.turn_off(Unit)

        self.onHeartbeat()
        return 

    def onHeartbeat(self):
        
        d = tinytuya.OutletDevice(Parameters["Username"], Parameters["Address"], Parameters["Password"])
        d.set_version(3.3)

        data = d.status()
        
        for i in range(1, int(Parameters["SerialPort"]) + 1):
            Devices[i].Update(int(data["dps"][str(i)]), str(data["dps"][str(i)]))

        return
    
    
global _plugin
_plugin = TuyaRelay()

def onStart():
    global _plugin
    _plugin.onStart()

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
