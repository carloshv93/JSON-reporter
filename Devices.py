import requests,Device,Globals,statistics

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
            self.devices.append(Device.Device(device["objid"],device["host"],device["device"]))

    def searchDevicesBySensor(self,name):
        devices = list()
        for device in self.devices:
            for sensor in device.sensors:
                if(sensor.ifKey(name)):
                    devices.append(sensor.ifKey())
        return devices

    def getAverages(self):
        averages = list()
        values = list()
        for device in self.devices:
                averages.append(device.getAverages())  
        keys = averages.pop(0).keys()
        for key in keys:
            for average in averages:
                values.append(average[key])
            
            self.averages[key] = statistics.mean(values)
        return self.averages        

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