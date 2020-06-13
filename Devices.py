import requests,statistics
from device import Device
import Globals

class Devices:
    id = None
    devices = list()
    averages = {}

    def __init__(self,objid):
        self.id = objid
        self.devices = list()
        self.averages = {}

    def addDevices(self):
        devicesRequest = requests.get("https://monitoreo.datasys.la/api/table.json?content=devices&output=json&columns=objid,host,device&count=10000&id="+str(self.id)+"&username="+Globals.user+"&password="+Globals.password)
        devicesJSON = devicesRequest.json()
        for device in devicesJSON["devices"]:
            self.devices.append(Device(device["objid"],device["host"],device["device"]))

    def copy(self,devices):
        self.devices = devices

    def searchDevicesBySensor(self,name):
        devices = list()
        for device in self.devices:
            for sensor in device.sensors:
                if(sensor.ifKey(name)):
                    devices.append(sensor.ifKey())
        return devices

    def agregarSensores(self):
        for device in self.devices:
            device.addSensors()

    def getAverages(self):
        averages = list()
        values = list()
        if self.devices != list():
            for device in self.devices:
                    averages.append(device.getAverages())  
            keys = averages[0].keys()
            for key in keys:
                for average in averages:
                    if average != {}:
                        values.append(average[key])
                if values != list():
                    self.averages[key] = statistics.mean(values)
        return self.averages        

    def getGroupAverages(self, sensorValue, sensorKey):
        for device in self.devices:
            for sensor in device.sensors:
                if "Disk Free" in sensor.name:
                    sensor.name = sensor.name.split(":\\",1)[0]
                    sensor.addHistoricData()
                    sensor.avgByKey(sensorKey)
                if sensor.name in sensorValue:
                    sensor.addHistoricData()
                    sensor.avgByKey(sensorKey)
            device.getAverages()

    def toJSON(self):
        data = {"objid":str(self.id),"devices count": len(self.devices),"averages": self.averages}
        data[str("devices")] = []
        for device in self.devices:
            data[str("devices")].append(device.toJSON())
        return data
        
    def toString(self):
        result = "objid:"+str(self.id)+  "\t devices count: "+ str(len(self.devices))+ "\taverages:"+ str(self.averages)
        for device in self.devices:
            result = result + "\n\t"  + device.toString()
        return result