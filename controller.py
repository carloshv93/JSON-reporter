# -----------------------------------------------------------
# Extraxión datos reporte BPD-6881
#
# 2020 Carlos Herrera, Datasys Group, Costa Rica
# email carlos.herrerda@datasys.la
# email carloshv93@gmail.com
# -----------------------------------------------------------

#Importación de librerías necesaias 
from devices import Devices
from device import Device
from sensor import Sensor
import Globals 
import json


class Controller():

    def __init__(self):
        self.duration = 1000  # milliseconds
        self.freq = 440  # Hz
        #variables globales     
        # "RoutersCore":117703   
        self.groups = {"Routers":70664,"Switches":105275,"Balanceadores":111038,"SAS":109954}
        self.groupsTemp = {"SAS":109954}
        
        #more variables

    def createJSONFile(self,object,name):
        with open(name, 'w') as outfile:
            json.dump(object, outfile)


    def printResults(self,format,sensor,group):
        if format == "json":
            print ("Dispositivos con umbral superado: " + str(len(self.devicesOverThreshold.devices)))
            print ("Dispositivos con sensores no deseados: " + str(len(self.devicesNotContains.devices)))
            print ("Dispositivos dentro del reporte: " + str(len(self.devicesFiltered.devices)))
            print ("Dispositivos sin sensores deseados:  " + str(len(self.devicesWithoutSensors.devices)))
            self.group = self.devicesOverThreshold
            self.group.getAverages()
            self.createJSONFile(self.group.toJSON(),group + " " + sensor + " Umbrales superados.json")

            self.group = self.devicesNotContains
            self.group.getAverages()
            self.createJSONFile(self.group.toJSON(), group + " " + sensor + " Dispositivos con sensores no deseados.json")
            
            self.group = self.devicesFiltered
            self.group.getAverages()
            self.createJSONFile(self.group.toJSON(), group + " " + sensor + " Dispositivos para reporte.json")
            
            self.group = self.devicesWithoutSensors
            self.group.getAverages()
            self.createJSONFile(self.group.toJSON(), group + " " + sensor + " Dispositivos sin sensores deseados.json")
        elif format == "txt":
            self.group.devices = self.devicesOverThreshold
            self.group.getAverages()
            print ("Dispositivos con unbral superado\n" + (self.group.toString()))
            self.group.devices = self.devicesNotContains
            self.group.getAverages()
            print ("Dispositivos con sensores no deseados\n" + self.group.toString())
            self.group.devices = self.devicesFiltered
            self.group.getAverages()
            print ("Dispositivos dentro del reporte\n" + self.group.toString())
            self.group.devices = self.devicesWithoutSensors
            self.group.getAverages()
            print ("Dispositivos sin sensores deseados\n" + self.group.toString())
                
    def filterDevicesBySensor(self,sensor):    
        devicesFiltered = list()     
        devicesWithoutSensors = list()
        for device in self.group.devices:
            if (device.containsSensor(sensor)):
                devicesFiltered.append(device)
            else:
                devicesWithoutSensors.append(device)
        self.devicesFiltered.copy(devicesFiltered)
        self.devicesWithoutSensors.copy(devicesWithoutSensors)

    def agrupa_no_permitidos(self):
        devicesNotContains = list()
        for device in self.group.devices:
            if (device.ifSensorNotAllowed(Globals.sensoresPermitidos)):
                self.devicesNotContains.devices = devicesNotContains      

    def separar_en_metodos(self):
        #Filtrar dispositivos basado en especificos sensores
        for (groupName,groupId) in self.groupsTemp.items():
            print (groupName)
            for (sensorKey,sensorValue) in Globals.sensors.items():
                print("\t" + sensorKey)
                if (sensorKey == "Storage"):
                    pass
                self.group = Devices(groupId)
                self.group.addDevices()
                self.group.agregarSensores()
                self.devicesOverThreshold = Devices(self.group.id)
                self.devicesNotContains = Devices(self.group.id)
                self.devicesFiltered = Devices(self.group.id)
                self.devicesWithoutSensors = Devices(self.group.id)
                self.filterDevicesBySensor(sensorValue)
                self.devicesFiltered.getGroupAverages(sensorValue,sensorKey)
                #Dispositivos con sensores no permitidos
                self.agrupa_no_permitidos()
                self.printResults("json",sensorKey,groupName)


    """
    writer = pd.ExcelWriter('CPU Avergae.xlsx', engine='xlsxwriter')
    device.avgBySensorName("CPU").to_excel(writer, 'Sheet1')
    writer.save()
    """