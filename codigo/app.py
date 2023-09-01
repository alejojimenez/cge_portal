import re
import os
import io
import pdfkit
import time
import requests
import openpyxl
import rpa as r
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, url, email, password, driver_path):
        print(url, email, password, driver_path)
        self.url = url
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.driver = None

    def wait(self, seconds):
        return WebDriverWait(self.driver, seconds)
    
    def close(self):
        self.driver.close()
        self.driver = None

    def quit(self):
        self.driver.quit()
        self.driver = None
        
    def login(self):
        print('Entrando en la funcion login...')
        
        # # Opciones de Chrome
        # chrome_options = Options()
        # chrome_options.add_experimental_option("prefs", {
        #     "download.default_directory": folder_path,
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "safebrowsing.enabled": True
        # })        
        
        self.driver = webdriver.Chrome(self.driver_path) # , chrome_options=chrome_options
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        
        # Seteo de las credenciales
        username = self.email
        password = self.password

        iframe = self.driver.find_element(By.ID,'content').find_element(By.TAG_NAME,'iframe')
        self.driver.switch_to.frame(iframe)
        
        rut_input = self.driver.find_element(By.CSS_SELECTOR,'input[name="txtRutLoginE"]')
        rut_input.send_keys(username)       

        password_input = self.driver.find_element(By.CSS_SELECTOR,'input[name="txtClaveLoginE"]')
        password_input.send_keys(password)       
        
        button_submit = self.driver.find_element(By.CSS_SELECTOR, 'input[name="imbIngresarLogin"]')
        button_submit.click()
        time.sleep(10)
        
        self.driver.switch_to.default_content()
        time.sleep(10)
        
        
    def scrape(self):
        # Aquí iría el código para navegar por la página y extraer la información deseada
        print('Entrando en la funcion scrape...')
        
        # Ruta completa de la carpeta "input" dentro de tu proyecto
        folder_path = os.path.join(os.getcwd(), "input")
        
        # Crear la carpeta "input" si no existe
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Leer Archivo de Excel Tabla de RUTs
        file_tabla_cliente = './config/clientes.xlsx'
        df_tabla_cliente = pd.read_excel(file_tabla_cliente, index_col=3)
        print('DataFrame Clientes: ', df_tabla_cliente)
        print('----------------------------------------------------------------------')

        # Variable tipo lista para almacenar los numero de clientes
        numero_cliente = [""]

        # adicionar a lista el valor de Clientes
        for cliente, row in df_tabla_cliente.iterrows():
            numero_cliente.append(str(cliente))

        numero_cliente.pop(0)    
        print('Lista de Clientes: ', numero_cliente)
        print('----------------------------------------------------------------------')

        # Obtiene el identificador de la ventana actual
        current_window = self.driver.current_window_handle
        print(current_window)
        print('----------------------------------------------------------------------')
            
        # Obtiene los identificadores de las ventanas abiertas
        window_handles = self.driver.window_handles
        print(window_handles, len(window_handles))
        print('----------------------------------------------------------------------')            
            
        # Cambiar al último manejo de ventana emergente
        self.driver.switch_to.window(window_handles[0])
        self.driver.implicitly_wait(25)

        div_right_content = self.driver.find_element(By.ID,'divRightContent').find_element(By.ID,'ctl00_ContentPlaceHolder1_fltCuentasUsuario_ddlNroClienteFCU')
        self.driver.switch_to.frame(div_right_content)

        intentos = 0
        reintentar = True
        #selector_seleccione = '//*[@id="ctl00_ContentPlaceHolder1_fltCuentasUsuario_ddlNroClienteFCU"]'
        selector_seleccione_1 = 'ctl00_ContentPlaceHolder1_fltCuentasUsuario_ddlNroClienteFCU'
        #selector_seleccione_2 = "ctl00$ContentPlaceHolder1$fltCuentasUsuario$ddlNroClienteFCU"
        
        while (reintentar):
            try:
                print('Try en la funcion click_element_xpath para el campo seleccione...', intentos)
                print('----------------------------------------------------------------------')
                intentos += 1
                self.wait(20).until(EC.presence_of_element_located((By.ID, selector_seleccione_1)))
                seleccione = self.driver.find_element(By.ID, selector_seleccione_1)
                seleccione.send_keys(numero_cliente)
                reintentar = False
            except Exception as e:    
                print('Exception en la funcion click_element_xpath', e)
                print('----------------------------------------------------------------------')

                reintentar = intentos <= 3

        # self.driver.switch_to.default_content()
        time.sleep(25)

        seleccione = self.driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_fltCuentasUsuario_ddlNroClienteFCU"]')
        seleccione.send_keys(numero_cliente[0])
        print('Cliente: ', numero_cliente[0])

        # div_left_content = self.driver.find_element(By.ID,'divLeftContent').find_element(By.ID,'divMi\ Cuenta > ul > li:nth-child(4) > a')
        # self.driver.switch_to.frame(div_left_content)

        # intentos = 0
        # reintentar = True
        # #selector_pagos = '//a[@href="/OVCGE.WebApp/Paginas/MiCuenta/PagosRealizados.aspx?id=E200"]' #'//*[@id="divMi Cuenta"]/ul/li[4]/a'
        # selector_pagos_1 = 'divMi\ Cuenta > ul > li:nth-child(4) > a'
        # #By.XPATH, '//a[@href="/OVCGE.WebApp/Paginas/MiCuenta/PagosRealizados.aspx?id=E200"]'
        # while (reintentar):
        #     try:
        #         print('Try en la funcion click_element_xpath para el campo pagos realizados...', intentos)
        #         print('----------------------------------------------------------------------')
        #         intentos += 1
        #         self.wait(20).until(EC.presence_of_element_located((By.ID, selector_pagos_1)))
        #         self.wait(20).until(EC.element_to_be_clickable((By.ID, selector_pagos_1)))
        #         pagos_realizados = self.driver.find_element(By.ID, selector_pagos_1)
        #         pagos_realizados.click()
        #         reintentar = False
        #     except Exception as e:    
        #         print('Exception en la funcion click_element_xpath', e)
        #         print('----------------------------------------------------------------------')

        #         reintentar = intentos <= 3
    
        # self.driver.switch_to.default_content()
        time.sleep(25)

        pagos_realizados = self.driver.find_element(By.XPATH, '//*[@id="divMi Cuenta"]/ul/li[4]/a')
        pagos_realizados.click()

        # # Seleccione cliente
        # selector_cliente = '//*[@id="ctl00_ContentPlaceHolder1_fltCuentasUsuario_ddlNroClienteFCU"]'
        # seleccione = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, selector_cliente)))
        # seleccione = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, selector_cliente)))
        # seleccione.send_keys(numero_cliente)
        # #seleccione.click()

        # # Click en Pagos realizados
        # selector_pagos = '//*[@id="divMi Cuenta"]/ul/li[4]/a'
        # pagos_realizados = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, selector_pagos)))
        # pagos_realizados = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, selector_pagos)))
        # pagos_realizados.click()

        #//*[@id="ctl00_ContentPlaceHolder1_gvwListaCuentas"]/tbody
        
        # Leer y capturar web table  --------->>>>
        try:
            caption_table = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#divContenido')))
            print('caption_table', caption_table)
            body_table = caption_table.find_element("xpath", "//tbody")
            self.driver.implicitly_wait(5)
        except:
            self.driver.refresh()
            print('Web table...')
            pass
        
        # Leer y capturar TR web table
        try:
            body_rows = body_table.find_elements("xpath", "//tr")
            print('Body Lineas: ', len(body_rows))
            self.driver.implicitly_wait(5)
        except:
            self.driver.refresh()
            print('TR web table...')
            pass
            
        count = 0
        if (len(body_rows) == 6):
            while (count < 4):
                try:
                    print('Refrescar Carga de Pagina....')
                    r.keyboard('[F5]')
                    self.driver.implicitly_wait(10)
                    
                    # Leer y capturar web table
                    caption_table = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#divContenido')))
                    body_table = caption_table.find_element("xpath", "//tbody")
                    self.driver.implicitly_wait(5)
            
                    # Leer y capturar TR web table
                    body_rows = body_table.find_elements("xpath", "//tr")
                    print('Body Lineas Navegador Refrescado: ', len(body_rows))
                    self.driver.implicitly_wait(5)

                    if (len(body_rows) == 6):
                        print('Reintentar actualizar navegador....')
                        count += 1
                        time.sleep(10)
                    else:
                        break

                except:
                    self.driver.refresh()
                    print('Continuar...')
                    count += 1
                    pass

        # Leer y capturar TD web table
        try:
            for row in body_rows:
                
                data = row.find_elements("xpath", '//*[starts-with(@id, "ctl") and contains(@id, "_updVerBoleta")]')
                print('Contenido Linea Data Mayor a 6: ', row)
                print('Data: ', len(data))
                self.driver.implicitly_wait(5)
                    
                file_row = []
                for data_cge in data:
                    data_cge_text = str(data_cge.text.encode("utf8"), 'utf-8')
                    print('Agregar data_cge_text: ', data_cge_text)
                    file_row.append(data_cge_text)

                time.sleep(15)            
                break

            print('Resultado: ', file_row)
            print('----------------------------------------------------------------------')
                    
        except:
            self.driver.refresh()
            print('TD web table...')
            pass

        # Encontrar los elementos en la página y hacer clic en ellos
        count = 0
        for document in file_row:
            # Encontrar el elemento por su valor de texto
            xpath = f"//*[text()='{document}']"
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Hacer clic en el numero de factura
            element.click()
            time.sleep(30)
            
            # Obtiene el identificador de la ventana actual
            current_window = self.driver.current_window_handle
            print(current_window)
            print('----------------------------------------------------------------------')
            
            # Obtiene los identificadores de las ventanas abiertas
            window_handles = self.driver.window_handles
            print(window_handles, len(window_handles))
            print('----------------------------------------------------------------------')            
            
            # Cambiar al último manejo de ventana emergente
            self.driver.switch_to.window(window_handles[-1])
            self.driver.implicitly_wait(5)
            
            # Obtener los bytes del archivo descargado
            file_bytes = self.driver.page_source.encode('utf-8')
            
            # Guardar los bytes en un archivo temporal
            temp_file = io.BytesIO(file_bytes)
            
            # Guardar el archivo temporal como PDF
            folder_path = './config/'
            pdf_path = os.path.join(folder_path, f"{str(cliente)}_{str(document)}.pdf") #"ruta_del_archivo.pdf"
            pdfkit.from_file(temp_file, pdf_path)            

            count += 1
            print('Conteo de documentos: ', count)
            print('----------------------------------------------------------------------')                
            
            # # Guardar los bytes en un archivo PDF
            # count += 1
            # file_path = os.path.join(folder_path, f"{str(cliente)}_{str(document)}.pdf")
            # with io.open(file_path, "wb") as file:
            #     file.write(file_bytes)
            #     print('Conteo de documentos: ', count)
            #     print('----------------------------------------------------------------------')                
                        
            # # Obtener la URL de la barra de direcciones
            # url_blob = self.driver.current_url
            # print(url_blob)
            # print('----------------------------------------------------------------------')            
                
            # # Descargar el archivo usando la URL blob
            # respuesta = requests.get(url_blob)
            # time.sleep(5)
            # contenido = respuesta.content
                
            # # Guardar el archivo en el disco
            # count += 1
            # with open(f'{str(cliente)}_{str(document)}.pdf', 'wb') as archivo:
            #     archivo.write(contenido)
            #     print('Conteo de documentos: ', count)
            #     print('----------------------------------------------------------------------')                

            # Cerrar la ventana emergente
            time.sleep(5)            
            self.driver.close()

            # Cambiar de nuevo al manejo de ventana principal
            self.driver.switch_to.window(window_handles[0])
                
        
        time.sleep(50)
        
        # Cerrar el driver de Selenium
        #self.driver.quit()
        
