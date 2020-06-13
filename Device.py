import requests,json
from sensor import Sensor
import Globals

class Device:
    id = None
    ip = None
    name = None
    averages = {}
    sensors = list()

    def __init__(self,objid,ip,name):
        self.id = objid
        self.ip = ip
        self.name = name
        self.sensors = list()
        self.averages = {}

    def addSensors(self):
        stringRequest = requests.get("https://monitoreo.datasys.la/api/table.json?content=sensors&output=json&columns=objid,sensor,name,host&count=10000&id="+str(self.id)+"&username="+Globals.user+"&password="+Globals.password)
        stringJSON = stringRequest.json()
        for sensor in stringJSON["sensors"]:
            self.sensors.append(Sensor(sensor["objid"],sensor["sensor"]))

    def containsSensor(self,names):
        result = False
        for sensor in self.sensors:
            if "Disk Free" in names and "Disk Free" in sensor.name:
                result = True
            if sensor.name in names:
                result = True
        return result

    def ifSensorNotAllowed(self,names):
        result = False
        for sensor in self.sensors:
            if sensor.name not in names:
                result = True
        return result
    
    def getAverages(self):
        for sensor in self.sensors:
            if sensor.average > 0:
                self.averages[sensor.averageKey] = sensor.average
        return self.averages        

    def toJSON(self):
        data = {"id":str(self.id),"name":str(self.name),"ip":str(self.ip), "sensors count": len(self.sensors),"averages":self.averages}
        data["sensors"] = []
        for sensor in self.sensors:
            if sensor.average != 0 :
                data["sensors"].append(sensor.toJSON())
        return data        

    def toString(self):
        resultado = "Device: "+str(self.id)+"\tip: "+str(self.ip)+"\tname: "+str(self.name)+"\taverages: " + json.dumps(self.averages)
        for sensor in self.sensors:
            if sensor.average != 0 :
                resultado = resultado + "\n\t" + sensor.toString()
        return resultado