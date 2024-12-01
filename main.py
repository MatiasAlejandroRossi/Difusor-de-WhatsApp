from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def iniciar_sesion():
    # Configura el WebDriver utilizando la clase Service
    service = Service('C:/Users/matii/Desktop/Directorios/PROYECTOS/chromedriver-win64/chromedriver.exe')  # Cambia a la ruta donde está tu ChromeDriver
    driver = webdriver.Chrome(service=service)
    driver.get("https://web.whatsapp.com/")
    
    # Da tiempo para escanear el código QR
    print("Escanea el código QR para iniciar sesión en WhatsApp Web.")
    time.sleep(15)  # Ajusta según el tiempo necesario para escanear
    
    return driver

def obtener_miembros_del_grupo(driver, nombre_grupo):
    # Busca el grupo por su nombre
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(nombre_grupo)
    search_box.send_keys(Keys.ENTER)
    
    time.sleep(3)
    
    # Abre la lista de miembros
    driver.find_element(By.XPATH, '//div[@class="_amie"][@role="button"]').click()
    time.sleep(3)
    
    # Extrae los nombres de los miembros
    miembros = []
    elementos = driver.find_elements(By.XPATH, '//span[@dir="auto"]')
    for elemento in elementos:
        miembros.append(elemento.text)
    
    print(f"Miembros obtenidos: {miembros}")
    return miembros

def enviar_mensaje_privado(driver, miembro, mensaje):
    # Buscar al miembro por su nombre
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(miembro)
    search_box.send_keys(Keys.ENTER)
    
    time.sleep(2)
    
    # Enviar el mensaje
    input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@data-tab="10"]')
    input_box.send_keys(mensaje)
    input_box.send_keys(Keys.ENTER)

def main():
    driver = iniciar_sesion()
    nombre_grupo = "Los Abandonados"  # Cambia esto por el nombre real del grupo
    mensaje = "Hola, este es un mensaje automático enviado de manera personalizada."
    
    try:
        # Obtener miembros del grupo
        miembros = obtener_miembros_del_grupo(driver, nombre_grupo)
        # Enviar mensajes a cada miembro
        for miembro in miembros:
            enviar_mensaje_privado(driver, miembro, mensaje)
            time.sleep(1)  # Pausa para evitar sobrecarga
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Asegurar el cierre del navegador
        driver.quit()
        print("Navegador cerrado correctamente.")

if __name__ == "__main__":
    main()
