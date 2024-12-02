from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_sesion():
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    print("Escanea el código QR para iniciar sesión en WhatsApp Web.")
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
    )
    print("Inicio de sesión exitoso.")
    return driver

def buscar_grupo(driver, grupo):
    # Buscar el cuadro de búsqueda
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @role="textbox" and @data-tab="3"]'))
    )
    search_box.clear()
    search_box.send_keys(grupo)
    search_box.send_keys(Keys.ENTER)
    print(f"Grupo '{grupo}' encontrado y seleccionado.")

def acceder_info_grupo(driver):
    # Acceder al botón de información del grupo
    info_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@class="x1c4vz4f x2lah0s xdl72j9 x1i4ejaq x1y332i5" and @role="button"]'))
    )
    info_button.click()
    print("Información del grupo abierta.")

def expandir_lista(driver):
    try:
        # Verificar si aparece el botón "Ver todos"
        ver_todos_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="_alzb  xnnlda6 xh8yej3 x8x1vt3 x78zum5 x6s0dn4 x16cd2qt x1z0qo99" and @role="button"]'))
        )
        ver_todos_button.click()
        print("Lista expandida.")
    except:
        print("Botón 'Ver todos' no encontrado o ya expandido.")

def enviar_mensaje(driver, mensaje):
    # Localizar el cuadro de texto y enviar mensaje
    message_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @tabindex="10" and contains(@class, "x1hx0egp")]'))
    )
    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)
    print("Mensaje enviado.")

def procesar_miembros(driver, mensaje, procesados):
    while True:
        # Obtener elementos dinámicos
        elementos = driver.find_elements(By.XPATH, '//div[contains(@class, "x10l6tqk xh8yej3 x1g42fcv") and @role="button"]')
        nuevos = False

        for elemento in elementos:
            style = elemento.get_attribute("style")
            if not style:
                continue

            # Extraer el valor de z-index
            try:
                z_index = int(style.split("z-index: ")[1].split(";")[0])
            except (IndexError, ValueError):
                continue

            if z_index in procesados:
                continue  # Ya procesado

            nuevos = True
            procesados.add(z_index)
            print(f"Procesando elemento con z-index: {z_index}")

            # Hacer clic en el miembro
            elemento.click()
            time.sleep(2)

            # Enviar mensaje
            enviar_mensaje(driver, mensaje)

            # Volver atrás
            driver.back()
            time.sleep(2)
            break  # Reiniciar la búsqueda después de procesar un miembro

        if not nuevos:
            try:
                # Deslizar hacia abajo para cargar más elementos dinámicos
                lista = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "scrollable-list-class")]'))
                )
                driver.execute_script("arguments[0].scrollTop += 300;", lista)
                time.sleep(2)
            except:
                print("No hay más elementos por procesar. Finalizando.")
                break

def main():
    grupo = "Ing. Sistemas - 1k9"
    mensaje = "Hola"
    procesados = set()

    driver = iniciar_sesion()
    
    try:
        while True:
            buscar_grupo(driver, grupo)
            acceder_info_grupo(driver)
            expandir_lista(driver)
            procesar_miembros(driver, mensaje, procesados)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Programa finalizado.")
        driver.quit()

if __name__ == "__main__":
    main()
