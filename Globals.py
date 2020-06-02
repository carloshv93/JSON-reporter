global user 
user = "service-desk"

global password 
password = "Datasys.19"

global sdate 
startdate = "2020-05-21-00-00-00"
global edate 

enddate = "2020-06-01-00-00-00"
global interval 
interval = "3600" #En segundos. 3600 = 1h

global thresholdCPU #Limite de uso del CPU
thresholdCPU = 2.00
<<<<<<< HEAD

global thresholdRAM #Limite de RAM disponible
thresholdRAM = 89.00

sensorsCPU = ["System Health CPU","SNMP Carga de CPU","CPU Load","Carga de procesador"]
sensorsRAM = ["System Health Memoria","System Health Memory"]
global sensors
sensors = {"CPU":sensorsCPU,"Percent Available Memory":sensorsRAM} #Percent Available Memory = RAM

global sensoresPermitidos
sensoresPermitidos = ["Carga de procesador","System Health CPU","SNMP Carga de CPU","CPU Load","Ping","System Health Memoria","System Health Memory","Uptime","Disponibilidad SNMP"]
=======
global thresholdRAM #Limite de uso de RAM
thresholdRAM = 89.00
#bado was here
>>>>>>> origin
