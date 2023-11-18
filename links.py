from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
def is_iterable(obj):
    """
    Check if an object is iterable.

    Args:
    obj: Object to be checked.

    Returns:
    bool: True if the object is iterable, False otherwise.
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False
    
# Set up Firefox options
options = Options()
options.headless = False  # Set to False if you want to see the Firefox window

# Initialize the WebDriver
driver = webdriver.Firefox(options=options)

# Navigate to the page
url = 'https://www.fan.es/index.php/natacion/eventos-provinciales/calendario-cadiz'
driver.get(url)

# Wait for the dropdown to be clickable
wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="limit"]')))

# Click on the dropdown to show options
dropdown.click()

# Now, select the 'Todos' option
# Since the 'Todos' option is a value in the dropdown, we can set it directly
all_option = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section[4]/div/div/div[1]/section/div/div/div/div/div/div/div[3]/div[6]/form/div/div/select/option[9]')))

all_option.click()

# Wait for the page to refresh with all the rows visible
wait.until(EC.staleness_of(all_option))

# At this point, you can start scraping the data as all rows should now be visible

# Get all the rows
rows = driver.find_elements(By.CLASS_NAME, 'ev_link_row')
urls_linksweb = []
for row in rows:
    urls_linksweb.append(row.get_attribute('href'))

# Now, you can loop through the urls and scrape the data
urls = []
for url in urls_linksweb:
    print('Scraping: ' + url + ' ..............')
    driver.get(url)
    # Do your scraping here
    # get the a which has text 'WEB DE RESULTADOS'
    try:
        web_results = driver.find_element(By.PARTIAL_LINK_TEXT, 'WEB DE RESULTADOS')
    except:
        web_results = driver.find_elements(By.PARTIAL_LINK_TEXT, 'WEB DEL CAMPEONATO')
        
    if (is_iterable(web_results)):
        for web in web_results:
            urls.append(web.get_attribute('href'))
            print('hemos conseguido        ' + web.get_attribute('href') + '\n')
    else:
        urls.append(web_results.get_attribute('href'))
        print('hemos conseguido        ' + web_results.get_attribute('href') + '\n')

# Dictionary wit urls_linksweb as keys and urls as values
url_dict = dict(zip(urls_linksweb, urls))

# save dictionary as json file
import json
with open('urls.json', 'w') as fp:
    json.dump(url_dict, fp)
# Close the WebDriver
driver.quit()
