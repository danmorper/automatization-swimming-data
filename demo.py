import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sys
# import urls.json file
import json
with open('overall_results.json') as f:
    dict_urls = json.load(f)

# Receive the city name as an argument
city_name = sys.argv[1]
# Get the URL for the city
urls = dict_urls[city_name]

# Set up Firefox options
options = Options()
options.headless = True  # Set to False if you want to see the Firefox window

# Use the options to specify the driver path
driver = webdriver.Firefox(options=options)

for url in urls.values():
    print("url is: {}".format(url))
    # Open the URL in the browser
    driver.get(url)
    # print the title of the page
    # print(driver.title)

    # Find all <a> tags with "Resultados" in the text and click on it
    resultados_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Resultados')

    # Create a new directory with name cityname inside of pdfs to store the pdfs
    os.makedirs(os.path.join("pdfs", city_name), exist_ok=True)
    output_dir = os.path.join("pdfs", city_name)
    pdfs = []
    try:
        del resultados_links[0]
    except:
        pass
    try:
        for link in resultados_links:
            pdfs.append(link.get_attribute('href'))
    except:
        pass

    # Create a new directory inside of pdfs to store the pdfs
    new_folder_name = url.split('/')[-1]
    if new_folder_name == '':
        new_folder_name = url.split('/')[-2]
    new_folder_path = os.path.join(output_dir, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    #Find text in the page which contains 'Piscina Corta'
    if 'Piscina Corta' in driver.page_source:
        # Create a file called piscina_corta.txt inside of the new folder
        with open(os.path.join(new_folder_path, 'piscina_corta.txt'), 'w') as f:
            f.write('forsa clu natasion jere lolololololo')

    for pdf in pdfs:
        r = requests.get(pdf)
        if r.status_code == 200:
            file_path = os.path.join(new_folder_path, os.path.basename(pdf))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(r.content)


    # print list of files in pdfs directory
# Close the browser
driver.close()