# -----------------------------------------------------------
# Extraxión datos reporte BPD-6881
#
# 2020 Carlos Herrera, Datasys Group, Costa Rica
# email carlos.herrerda@datasys.la
# email carloshv93@gmail.com
# -----------------------------------------------------------

#Importación de librerías necesaias 
from controller import Controller
import winsound,json

if __name__=='__main__':
    controller = Controller()
    controller.separar_en_metodos()