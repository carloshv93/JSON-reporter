import requests,Globals,json,statistics
class Sensor:
    id = None
    name = None
    historic = list()
    keys = list()
    average = 0.0
    averageKey = None

    def __init__(self,objid,name):
        self.id = objid
        self.name = name
        self.keys = list()
        self.historic = list()
        self.average= 0.0
        self.averageKey = None  
    
    def addHistoricData(self):
        devicesRequest = requests.get("https://monitoreo.datasys.la/api/historicdata.json?id="+str(self.id)+"&avg="+Globals.interval+"&sdate="+Globals.startdate+"&edate="+Globals.enddate+"&usecaption=1&username="+Globals.user+"&password="+Globals.password)
        devicesJSON = devicesRequest.json()
        temp = devicesJSON["histdata"][0].keys()
        for key in temp:
            self.keys.append(key)
        for data in devicesJSON["histdata"]:
            self.historic.append(data)

    def searchKey(self,name):
        if name == "CPU":
            self.averageKey = "CPU"
            if self.name in Globals.sensorsCPU:
                if (self.ifKey("Total")):
                    return "Total"
                else: 
                    for key in self.keys:
                        if name in key:
                            return key
        elif name == "RAM":
            if self.name in Globals.sensorsRAM:
                for key in self.keys:
                    if (("Percent" in key and "Processor" in key) or "Porcentaje de memoria disponible" in key):
                        if "Virtual" in self.name:
                            self.averageKey = "Virtual RAM"
                        elif "Physical" in self.name:
                                self.averageKey = "Physical RAM"
                        else:
                            self.averageKey = "RAM"
                        return key
        elif name == "Storage":
            for key in self.keys:
                if key == "Espacio libre":
                    self.averageKey = self.name
                    return key


    def ifKey(self,name):
        result = False
        for key in self.keys:
            if(name == key):
                result = True
        return result

    def avgByKey(self,names):
        values = []
        key = self.searchKey(names)
        if self.averageKey != None:
            for data in self.historic:
                if data.get(key) == "":
                    values.append(0.0)
                else:
                    values.append(data.get(key))  
            self.average =  statistics.mean(values)
        return self.average

    def checkThreshold(self,key):
        if "CPU" == key:
            return (self.average > Globals.thresholdCPU)
        elif "RAM" == key:
            return (self.average < Globals.thresholdRAM)
    def toJSON(self):
        data = {"id":str(self.id),"name":str(self.name),self.averageKey : str(self.average)}
        data["histdata"] = []
        for value in self.historic:
            data["histdata"].append(value)
        return data        
        
    def toString(self):
        return ("Sensor:"+str(self.name)+"\tobjid: "+str(self.id)+"\t "+ self.averageKey +":" + str(self.average) )