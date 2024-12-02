from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def iniciar_sesion():
    # Configurar el WebDriver utilizando la clase Service
    service = Service('C:/Users/matii/Desktop/Directorios/PROYECTOS/chromedriver-win64/chromedriver.exe')  # Cambia a la ruta dónde está tu ChromeDriver
    driver = webdriver.Chrome(service=service)
    driver.get("https://web.whatsapp.com/")

    # Da tiempo para escanear el código QR
    print("Escanea el código QR para iniciar sesión en WhatsApp Web.")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(By.XPATH, '//div[@contenteditable="true"][@role="textbox"][data-tab="3"]')
    )
    print("Inicio de sesión exitoso.")
    return driver

def buscar_grupo(driver, nombre_grupo):
    # Busca el grupo en el cuadro de búsqueda.
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@role="textbox"][@data-base="3"]')
    search_box.clear()
    search_box.send_keys(nombre_grupo)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)  # Espera para cargar el grupo.

def obtener_miembros_del_grupo(driver):
    # Abre la información del grupo
    group_info_button = driver.find_element(By.XPATH, '//header//div[@role="button][data-tab="3"]')
    group_info_button.click()
    time.sleep(2)

    # Si existe un botón "Ver todos", hacer click
    try:
        ver_todos_button = driver.find_element(By.XPATH, '//div[text()="Ver todos"]')
        ver_todos_button.click()
        time.sleep(2)
    except:
        print("No es necesario hacer clic en 'Ver todos'.")
    
    miembros = []
    miembros_elements = driver.find_elements(By.XPATH, '//div[@data-testid="cell-frame_container"]//span[@dir="auto"]')
    for miembro in miembros_elements:
        miembros.append(miembro.text)
    print(f"Miembros obtenidos: {miembros}")
    return miembros

def enviar_mensaje_a_miembro(driver, miembro, mensaje, nombre_grupo):
    miembro_element = driver.find_element(By.XPATH, f'//span[@dir="auto" and text()="{miembro}"]')
    miembro_element.click()
    time.sleep(2)

    try:
        enviar_mensaje_button = driver.find_element(By.XPATH, '//li[@role="button"]//span[contains(text(), "Enviar mensaje a")]')
        enviar_mensaje_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"No se pudi hacer clic en 'Enviar mensaje a' para {miembro}. Error: {e}")
        return False
    input_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(By.XPATH, '//div[@contenteditable="true"][@role="textbox][@data-tab="10"]')
    )
    input_box.send_keys(mensaje)
    input_box.send_keys(Keys.ENTER)
    print(f"Mensaje enviado a: {miembro}")
    driver.get("https://web.whatsapp.com/")
    time.sleep(3)
    buscar_grupo(driver, nombre_grupo)

    return True

def cargar_miembros_procesados():
    if os.path.exists("miembros_procesados.txt"):
        with open("miembros_procesados.txt", "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    return set()

def guardar_miembro_procesado(miembro):
    with open("miembros_procesados.txt", "a", encoding="utf-8") as file:
        file.write(f"{miembro}\n")

def main():
    driver = iniciar_sesion()
    nombre_grupo = "Los Abandonados"  # Cambiar por el nombre del grupo en el que se quiera difundir.
    mensaje = "Holiiiis, no respondan, mensaje de prueba. LO HICE :P MUAJAJAJAJAJ. Hackeamos bancos?"
    miembros_procesados = cargar_miembros_procesados()

    try:
        buscar_grupo(driver, nombre_grupo)
        miembros = obtener_miembros_del_grupo(driver)

        mensajes_enviados = 0
        for miembro in miembros_procesados:
            if enviar_mensaje_a_miembro(driver, miembro, mensaje, nombre_grupo):
                guardar_miembro_procesado(miembro)
                mensajes_enviados += 1
                time.sleep(2)

        # Verificación de envíos completos
        miembros_faltantes = set(miembros) - cargar_miembros_procesados()
        if not miembros_faltantes:
            print(f"Programa finalizado con éxito. Se enviaron {mensajes_enviados} mensajes.")
        else:
            print(f"Algunos miembros no recibieron el mensaje: {miembros_faltantes}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Asegurar el cierre del navegador
        driver.quit()
        print("Navegador cerrado correctamente.")

if __name__ == "__main__":
    main()
