from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import config

import json

def init():
    options = webdriver.ChromeOptions()
    
    # disable all graphics elements
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # if using Brave browser, this is the path to the binary
    options.binary_location = config.BINARY_LOCATION

    s = Service(config.DRIVER_PATH)

    return webdriver.Chrome(service=s, options=options)


def login(driver: webdriver.Chrome):
    email_input = driver.find_element(By.ID, "session_key")
    email_input.send_keys(config.MAIL)

    password_input = driver.find_element(By.ID, "session_password")
    password_input.send_keys(config.PASSWORD)

    submit_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
    submit_button.click()


def get_people(driver: webdriver.Chrome, text, pages = 1):
    search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=CLUSTER_EXPANSION&page={}"

    current_page = 1

    results = []
    while current_page <= pages:
        print(f"searching on page {current_page}")
        driver.get(search_url.format(text, current_page))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "entity-result__content")))
        elements = driver.find_elements(By.CLASS_NAME, "entity-result__content")
        

        for element in elements:
            # html = element.get_attribute('innerHTML')
            name = element.find_element(By.CLASS_NAME, "app-aware-link")
            position = element.find_element(By.CLASS_NAME, "entity-result__primary-subtitle")

            results.append({
                'name': name.text.split("\n")[0],
                'position': position.text
            })

        current_page += 1

    return results
 

def main():
    driver = init()
    driver.get('https://www.linkedin.com/')

    login(driver)

    results = get_people(driver, "uipath", 3)
    print(json.dumps(results, indent=4))

    driver.quit()


if __name__ == "__main__":
    main()
