# -----------------------------------------------------------
# Extraxión datos reporte BPD-6881
#
# 2020 Carlos Herrera, Datasys Group, Costa Rica
# email carlos.herrerda@datasys.la
# email carloshv93@gmail.com
# -----------------------------------------------------------

#Importación de librerías necesaias 
import Devices,Device,Sensor,Globals
import winsound,json


class controllerMain():

    def __init__(self):
        self.duration = 1000  # milliseconds
        self.freq = 440  # Hz
        #variables globales
        self.groups = [70664,117703,105275,111038]
        self.routersGroupId = 70664
        self.servidoresGroupId = 109954
        self.routersCoreGroupId = 117703
        self.switchesGroupId = 105275
        self.balanceadoresGroup = 111038

        #more variables
        group = Devices.Devices(routersGroupId)
        devicesOverThreshold = list()
        devicesFiltered = list()
        devicesNotContains = list()
        devicesWithoutSensors = list()
        group.addDevices()

    def createJSONFile(self,object,name):
        with open(name, 'w') as outfile:
            json.dump(object, outfile)


    def printResults(self,format,sensor):
        if format == "json":
            print ("Dispositivos con umbral superado: " + str(len(self.devicesOverThreshold)))
            print ("Dispositivos con sensores no deseados: " + str(len(self.devicesNotContains)))
            print ("Dispositivos dentro del reporte: " + str(len(self.devicesFiltered)))
            print ("Dispositivos sin sensores deseados:  " + str(len(self.devicesWithoutSensors)))
            self.group.devices = self.devicesOverThreshold
            self.group.getAverages()
            createJSONFile(self.group.toJSON(),"Dispositivos con umbrales superados " + sensor +".json")
            self.group.devices = self.devicesNotContains
            self.group.getAverages()
            createJSONFile(self.group.toJSON(),"Dispositivos con sensores no deseados " + sensor +".json")
            self.group.devices = self.devicesFiltered
            self.group.getAverages()
            createJSONFile(self.group.toJSON(),"Dispositivos para reporte " + sensor +".json")
            self.group.devices = self.devicesWithoutSensors
            self.group.getAverages()
            createJSONFile(self.group.toJSON(),"Dispositivos sin sensores deseados " + sensor +".json")
        elif format == "txt":
            group.devices = self.devicesOverThreshold
            self.group.getAverages()
            print ("Dispositivos con unbral superado\n" + (self.group.toString()))
            self.group.devices = self.devicesNotContains
            self.group.getAverages()
            print ("Dispositivos con sensores no deseados\n" + self.group.toString())
            group.devices = self.devicesFiltered
            self.group.getAverages()
            print ("Dispositivos dentro del reporte\n" + self.group.toString())
            self.group.devices = self.devicesWithoutSensors
            self.group.getAverages()
            print ("Dispositivos sin sensores deseados\n" + self.group.toString())
                


    def separar_en_metodos(self):
        #Filtrar dispositivos basado en especificos sensores
        for (sensorKey,sensorValue) in Globals.sensors.items():
            #Creación de dispositivos
            #Agregar sensores a los dispositivos 
            for device in self.group.devices:
                device.addSensors()
            for device in self.group.devices:
                if (device.containsSensor(sensorValue)):
                    self.devicesFiltered.append(device)
                    for sensor in device.sensors:
                        if sensor.name in sensorValue:
                            sensor.addHistoricData()
                            sensor.avgByKey(sensorKey)          
                            if (sensor.checkThreshold(sensor.averageKey)):
                                self.devicesOverThreshold.append(device)
                    device.getAverages()
                else:
                    self.devicesWithoutSensors.append(device) 
            #Dispositivos con sensores no permitidos
            for device in self.group.devices:
                if (device.ifSensorNotAllowed(Globals.sensoresPermitidos)):
                    self.devicesNotContains.append(device)
            printResults("json",sensorKey)


    """
    writer = pd.ExcelWriter('CPU Avergae.xlsx', engine='xlsxwriter')
    device.avgBySensorName("CPU").to_excel(writer, 'Sheet1')
    writer.save()

    winsound.Beep(freq, duration)
    """
