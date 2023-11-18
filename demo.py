import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# import urls.json file
import json
with open('urls.json') as f:
    urls = json.load(f)

# Set up Firefox options
options = Options()
options.headless = True  # Set to False if you want to see the Firefox window

# Use the options to specify the driver path
driver = webdriver.Firefox(options=options)

for url in urls.values():

    # Open the URL in the browser
    driver.get(url)

    # print the title of the page
    # print(driver.title)

    # Find all <a> tags with "Resultados" in the text and click on it
    resultados_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Resultados')

    output_dir = "pdfs"
    pdfs = []
    del resultados_links[0]
    for link in resultados_links:
        pdfs.append(link.get_attribute('href'))


for pdf in pdfs:
    r = requests.get(pdf)
    if r.status_code == 200:
        file_path = os.path.join(output_dir, os.path.basename(pdf))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(r.content)
            print("File downloaded successfully")
            print("Saved in {}".format(file_path))

# print list of files in pdfs directory
print(os.listdir(output_dir))
# Close the browser
driver.close()