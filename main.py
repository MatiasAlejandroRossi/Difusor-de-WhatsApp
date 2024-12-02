import pandas as pd
import webbrowser as web
import pyautogui as pg
import time

data = pd.read_excel("numeros_grupo_wpp.xlsx", sheet_name='Hoja1')
data.head(3)

for i in range(len(data)):
    celular = str(data.loc[i,'CEL']) # Convertir a string para que se añada al mensaje
    
    # Crear mensaje personalizado
    mensaje = "hola!"
    
    # Abrir una nueva pestaña para entrar a WhatsApp Web
    # Opción 1: Si te abre WhastApp Web directamente en Google Chrome
#     web.open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje)
    
    # Opción 2: Si te abre WhastApp Web en Microsoft Edge, especificar que lo abra en Chrome
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    web.get(chrome_path).open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje)
    
    time.sleep(8)           # Esperar 8 segundos a que cargue
    pg.click(1219,983)      # Hacer click en la caja de texto
    time.sleep(2)           # Esperar 2 segundos 
    pg.press('enter')       # Enviar mensaje 
    time.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
    pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
    time.sleep(2)