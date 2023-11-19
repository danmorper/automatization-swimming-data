from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()  # Initialize your WebDriver

driver.get("https://rfen.es/es/clubs")

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
def remove_whitespace(input_str):
    s = input_str
    s = s.replace(' ','')
    return s

# Create empty dataframe with 3 columns 'comunidad_autonoma', 'provincia', 'clubes'
df = pd.DataFrame({'comunidad_autonoma': [], 'provincia': [], 'clubes': []})

# Get max number of pages
num = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div/div[1]/div/div[2]/div/div[2]/div[4]/div[2]/span[1]').text
num = int(num[-3:])
print(num)
# Iterate over each page
for i in range(num):
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'colstyle-delegacion')))
    # find.element tbody
    div = driver.find_element(By.CLASS_NAME, 'ml-bottom')
    table = div.find_element(By.TAG_NAME, 'tbody')
    # iterate over each row of the table
    clubes = []
    provincias = []
    comunidades = []
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        # iterate over each cell of the row
        for cell in row.find_elements(By.TAG_NAME, 'td'):
            # print the cell text
            if cell.get_attribute('class') == 'colstyle-delegacion':
                delegacion = cell.text
                # split the text by |
                delegacion = delegacion.split("|")
                # apply remove_accents and make_lowercase to each element of delegacion
                delegacion = [make_lowercase(element) for element in delegacion]
                delegacion = [remove_accents(element) for element in delegacion]
                delegacion = [remove_whitespace(element) for element in delegacion]
                if delegacion == ['']:
                    comunidades.append(None)
                    provincias.append(None)
                elif len(delegacion) == 1:
                    comunidades.append("RFEN")
                    provincias.append(None)
                else:
                    comunidades.append(delegacion[0])
                    provincias.append(delegacion[1])
            elif cell.get_attribute('class') == 'colstyle-nombre':
                club = cell.text
                club = make_lowercase(club)
                club = remove_accents(club)
                club = remove_whitespace(club)
                clubes.append(club)
    temp_df = pd.DataFrame({'comunidad_autonoma': comunidades, 'provincia': provincias, 'clubes': clubes})
    df = pd.concat([df, temp_df], ignore_index=True)
    print(df)
    if i < (num-1):
        arrow = WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fa-angle-right')))
        driver.execute_script("arguments[0].click();", arrow)

print("for loop finished" + str(i) + "OLE YO PIXA") 
df.to_csv('clubs.csv', index=False)  # Save the dataframe to a CSV file
driver.close()  # Close the browser

print(sum(df["comunidad_autonoma"]=='Andalucía'))