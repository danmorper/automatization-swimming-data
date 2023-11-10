from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Firefox()  # Initialize your WebDriver

driver.get("https://rfen.es/es/clubs")
arrow = driver.find_element(By.CSS_SELECTOR, 'a.ml-trigger:nth-child(2)')

# Create empty dataframe with 3 columns 'comunidad_autonoma', 'provincia', 'clubes'
df = pd.DataFrame({'comunidad_autonoma': [], 'provincia': [], 'clubes': []})
                   
for i in range(1353):
    # Find elements using By for 'delegacion'
    delegacion_elements = driver.find_elements(By.CLASS_NAME, 'colstyle-delegacion')

    # Find elements using By for 'nombres'
    nombres_elements = driver.find_elements(By.CLASS_NAME, 'colstyle-nombre')

    # Hacer un diccionario en el que la clave sea la delegación y el valor sea el club
    # Access and print the text content of 'delegacion' elements
    delegaciones = []
    for element in delegacion_elements:
        delegaciones.append(element.text)
    # Separar en cada elemento de delegacion por | 

    delegaciones = [delegacion.split("|") for delegacion in delegaciones]
    # drop first element of delegaciones
    delegaciones = delegaciones[1:]
    
    comunidad_autonoma = []
    for delegacion in delegaciones:
        comunidad_autonoma.append(delegacion[0])
    
    provincia = []
    for delegacion in delegaciones:
        provincia.append(delegacion[1])
    print(delegaciones)

    # Access and print the text content of 'nombres' elements
    clubes = []
    for element in nombres_elements:
        clubes.append(element.text)
    clubes = clubes[1:]

    # change accents to non accents in the 3 lists and make them lowercase
    def remove_accents(input_str):
        s = input_str
        s = s.replace('á','a')
        s = s.replace('é','e')
        s = s.replace('í','i')
        s = s.replace('ó','o')
        s = s.replace('ú','u')
        return s
    def make_lowercase(input_str):
        s = input_str
        s = s.lower()
        return s
    comunidad_autonoma = [remove_accents(comunidad) for comunidad in comunidad_autonoma]
    comunidad_autonoma = [make_lowercase(comunidad) for comunidad in comunidad_autonoma]
    provincia = [remove_accents(provincia) for provincia in provincia]
    provincia = [make_lowercase(provincia) for provincia in provincia]
    clubes = [remove_accents(club) for club in clubes]
    clubes = [make_lowercase(club) for club in clubes]
    # Create a dataframe with the lists
    df.combine_first(pd.DataFrame({'comunidad_autonoma': comunidad_autonoma, 'provincia': provincia, 'clubes': clubes}))
    
    # Create a json file with the dataframe
    driver.execute_script("arguments[0].click();", arrow)

df.to_json('clubs.json', orient='records')
driver.close()  # Close the browser