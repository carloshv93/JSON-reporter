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
duration = 1000  # milliseconds
freq = 440  # Hz


#variables globales
groups = [70664,117703,105275,111038]
routersGroupId = 70664
servidoresGroupId = 109954
routersCoreGroupId = 117703
switchesGroupId = 105275
balanceadoresGroup = 111038

def createJSONFile(object,name):
    with open(name, 'w') as outfile:
        json.dump(object, outfile)


def printResults(format,sensor):
    if format == "json":
        print ("Dispositivos con umbral superado: " + str(len(devicesOverThreshold)))
        print ("Dispositivos con sensores no deseados: " + str(len(devicesNotContains)))
        print ("Dispositivos dentro del reporte: " + str(len(devicesFiltered)))
        print ("Dispositivos sin sensores deseados:  " + str(len(devicesWithoutSensors)))
        group.devices = devicesOverThreshold
        group.getAverages()
        createJSONFile(group.toJSON(),"Dispositivos con umbrales superados " + sensor +".json")
        group.devices = devicesNotContains
        group.getAverages()
        createJSONFile(group.toJSON(),"Dispositivos con sensores no deseados " + sensor +".json")
        group.devices = devicesFiltered
        group.getAverages()
        createJSONFile(group.toJSON(),"Dispositivos para reporte " + sensor +".json")
        group.devices = devicesWithoutSensors
        group.getAverages()
        createJSONFile(group.toJSON(),"Dispositivos sin sensores deseados " + sensor +".json")
    elif format == "txt":
        group.devices = devicesOverThreshold
        group.getAverages()
        print ("Dispositivos con unbral superado\n" + (group.toString()))
        group.devices = devicesNotContains
        group.getAverages()
        print ("Dispositivos con sensores no deseados\n" + group.toString())
        group.devices = devicesFiltered
        group.getAverages()
        print ("Dispositivos dentro del reporte\n" + group.toString())
        group.devices = devicesWithoutSensors
        group.getAverages()
        print ("Dispositivos sin sensores deseados\n" + group.toString())
               



#Filtrar dispositivos basado en especificos sensores
for (sensorKey,sensorValue) in Globals.sensors.items():
    #Creación de dispositivos
    group = Devices.Devices(routersGroupId)
    devicesOverThreshold = list()
    devicesFiltered = list()
    devicesNotContains = list()
    devicesWithoutSensors = list()
    group.addDevices()
    #Agregar sensores a los dispositivos 
    for device in group.devices:
        device.addSensors()
    for device in group.devices:
        if (device.containsSensor(sensorValue)):
            devicesFiltered.append(device)
            for sensor in device.sensors:
                if sensor.name in sensorValue:
                    sensor.addHistoricData()
                    sensor.avgByKey(sensorKey)          
                    if (sensor.checkThreshold(sensor.averageKey)):
                        devicesOverThreshold.append(device)
            device.getAverages()
        else:
            devicesWithoutSensors.append(device) 
    #Dispositivos con sensores no permitidos
    for device in group.devices:
        if (device.ifSensorNotAllowed(Globals.sensoresPermitidos)):
            devicesNotContains.append(device)
    printResults("json",sensorKey)

"""

writer = pd.ExcelWriter('CPU Avergae.xlsx', engine='xlsxwriter')
device.avgBySensorName("CPU").to_excel(writer, 'Sheet1')
writer.save()

"""

winsound.Beep(freq, duration)