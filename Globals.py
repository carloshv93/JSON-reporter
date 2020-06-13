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

global thresholdRAM #Limite de RAM disponible
thresholdRAM = 89.00


sensorsCPU = ["System Health CPU","SNMP Carga de CPU","CPU Load","Carga de procesador"]
sensorsRAM = ["System Health Memoria","System Health Memory","Memory: Physical Memory","Memory: Virtual Memory"]
sensorsStorage = ["Disk Free"]
global sensors
##"CPU":sensorsCPU,"RAM":sensorsRAM,
sensors = {"Storage":sensorsStorage} #Percent Available Memory = RAM

global sensoresPermitidos
sensoresPermitidos = ["Disk Free","Carga de procesador","System Health CPU","SNMP Carga de CPU","CPU Load","Ping","System Health Memoria","System Health Memory","Uptime","Disponibilidad SNMP"]
