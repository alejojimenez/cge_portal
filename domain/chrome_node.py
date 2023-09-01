
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..code.time_service import sleep


class ChromeNode():
    def __init__(self):
        print('ChromeNode init')
        #current_app.logger.info(f'Inicializando Chrome Node...')
        self.initialize_driver()

    def initialize_driver(self):
        driver = webdriver.Chrome(executable_path="./chromedriver") #, options=self.options
        self.driver = driver
        
    def wait(self, seconds):
        return WebDriverWait(self.driver, seconds)
    
    def close(self):
        self.driver.close()
        self.driver = None

    def quit(self):
        self.driver.quit()
        self.driver = None
        
    def click_element_id(self, selector):
        intentos = 0
        reintentar = True
        resultado = False
        while (reintentar):
            try:
                intentos += 1
                self.wait(10).until(EC.presence_of_element_located((By.ID, selector)))
                self.wait(10).until(EC.element_to_be_clickable((By.ID, selector)))
                elemento = self.driver.find_element(By.ID, selector)
                elemento.click()
                reintentar = False
                resultado = True
            except Exception as e:    
                sleep(10)
                reintentar = intentos <= 3
                resultado = False
        return resultado

    def click_element_xpath(self, selector):
        intentos = 0
        reintentar = True
        resultado = False
        while (reintentar):
            try:
                intentos += 1
                self.wait(10).until(EC.presence_of_element_located((By.XPATH, selector)))
                self.wait(10).until(EC.element_to_be_clickable((By.XPATH, selector)))
                elemento = self.driver.find_element(By.XPATH, selector)
                elemento.click()
                reintentar = False
                resultado = True
            except Exception as e:    
                sleep(10)
                reintentar = intentos <= 3
                resultado = False
        return resultado
    
    def set_text_element(self, selector, text):
        intentos = 0
        reintentar = True
        resultado = False
        while (reintentar):
            try:
                intentos += 1
                self.wait(10).until(EC.element_to_be_clickable((By.ID, selector)))
                elemento = self.driver.find_element(By.ID, selector)
                elemento.send_keys(text)
                reintentar = False
                resultado = True
            except Exception as e:
                sleep(10)
                reintentar = intentos <= 3
                resultado = False
        return resultado


