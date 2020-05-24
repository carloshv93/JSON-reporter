# -----------------------------------------------------------
# Extraxión datos reporte BPD-6881
#
# (C) 2020 Frank Carlos Herrera, Datasys Group, Costa Rica
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
routersCoreGroupId = 117703
switchesGroupId = 105275
balanceadoresGroup = 111038
sensorKeys = ["CPU","Percent Available Memory"]
devicesOverThreshold = list()
devicesFiltered = list()
devicesNotContains = list()
devicesWithoutSensors = list()
sensorsCPU = ["System Health CPU","SNMP Carga de CPU","CPU Load","Carga de procesador"]
sensorsRAM =["System Health Memoria","System Health Memory"]

sensorsToReport = sensorsCPU + sensorsRAM


sensoresPermitidos = ["Carga de procesador","System Health CPU","SNMP Carga de CPU","CPU Load","Ping","System Health Memoria","System Health Memory","Uptime","Disponibilidad SNMP"]




def createJSONFile(object,name):
    with open(name, 'w') as outfile:
        json.dump(object, outfile)


def printResults(format):
    if format == "json":
        print ("Dispositivos con umbral superado: " + str(len(devicesOverThreshold)))
        print ("Dispositivos con sensores no deseados: " + str(len(devicesNotContains)))
        print ("Dispositivos dentro del reporte: " + str(len(devicesFiltered)))
        print ("Dispositivos sin sensores deseados:  " + str(len(devicesWithoutSensors)))
        group.devices = devicesOverThreshold
        createJSONFile(group.toJSON(),"Dispositivos con umbrales superados.json")
        group.devices = devicesNotContains
        createJSONFile(group.toJSON(),"Dispositivos con sensores no deseados.json")
        group.devices = devicesFiltered
        createJSONFile(group.toJSON(),"Dispositivos para reporte.json")
        group.devices = devicesWithoutSensors
        createJSONFile(group.toJSON(),"Dispositivos sin sensores deseados.json")
    elif format == "txt":
        
        group.devices = devicesOverThreshold
        print ("Dispositivos con unbral superado\n" + (group.toString()))
        group.devices = devicesNotContains
        print ("Dispositivos con sensores no deseados\n" + group.toString())
        group.devices = devicesFiltered
        print ("Dispositivos dentro del reporte\n" + group.toString())
        group.devices = devicesWithoutSensors
        print ("Dispositivos sin sensores deseados\n" + group.toString())
               


#Creación de dispositivos
group = Devices.Devices(routersCoreGroupId)
group.addDevices()
#Agregar sensores a los dispositivos 
for device in group.devices:
    device.addSensors()

#Filtrar dispositivos basado en especificos sensores
for device in group.devices:
    if (device.containsSensor(sensorsToReport)):
        devicesFiltered.append(device)
        for sensor in device.sensors:
            if sensor.name in (sensorsToReport):
                sensor.addHistoricData()
                sensor.avgByKey(sensorKeys)          
                if (sensor.checkThreshold(sensor.averageKey)):
                   devicesOverThreshold.append(device)
        device.getAverages()
    else:
        devicesWithoutSensors.append(device)
        
group.getAverages()
#Dispositivos con sensores no permitidos
for device in group.devices:
    if (device.ifSensorNotAllowed(sensoresPermitidos)):
        devicesNotContains.append(device)


printResults("json")
printResults("txt")




"""
Sensor: Promedio
Dispositovo: {CPU:Promedio,RAM:Promedio}
group: {CPU:Promedio,RAM:Promedio}
Listar sensores que exceden umbral
"""


"""

writer = pd.ExcelWriter('CPU Avergae.xlsx', engine='xlsxwriter')
device.avgBySensorName("CPU").to_excel(writer, 'Sheet1')
writer.save()

"""

winsound.Beep(freq, duration)