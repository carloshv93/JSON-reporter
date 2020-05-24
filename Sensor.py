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

    def searchKey(self,names):
        for key in self.keys:
            for name in names:
                if name in key :
                    if name == "Percent Available Memory" and "Processor" in key:
                        self.averageKey = "RAM"
                    elif name != "Percent Available Memory":
                        self.averageKey = name
                    return key

    def ifKey(self,name):
        for key in self.keys:
            return (name in key)

    def avgByKey(self,names):
        values = []
        key = self.searchKey(names)
        if self.averageKey:
            for data in self.historic:
                if data.get(key) == "":
                    values.append(0.0)
                else:
                    values.append(data.get(key))  
            self.average =  statistics.mean(values)
        return self.average

    def checkThreshold(self,key):
        if "CPU" in key:
            return (self.average > Globals.thresholdCPU)
        elif "Percent Available Memory":
            return (self.average < Globals.thresholdRAM)
    def toJSON(self):
        data = {"id":str(self.id),"name":str(self.name),self.averageKey : str(self.average)}
        data["histdata"] = []
        for value in self.historic:
            data["histdata"].append(value)
        return data        
        
    def toString(self):
        return ("Sensor:"+str(self.name)+"\tobjid: "+str(self.id)+"\t "+ self.averageKey +":" + str(self.average) )