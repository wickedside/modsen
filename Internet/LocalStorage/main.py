from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_driver_path = '../chromedriver.exe'

# Chrome options
options = Options()
options.add_argument("--headless")  # launching without interface (no need)

# web-driver init
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # open web page
    driver.get('https://example.com')

    # set value in LocalStorage
    script_set = "window.localStorage.setItem('Key', 'Value');"
    driver.execute_script(script_set)

    # get value from LocalStorage
    script_get = "return window.localStorage.getItem('Key');"
    value = driver.execute_script(script_get)
    print("LocalStorage value:", value)

    # remove value from LocalStorage
    script_remove = "window.localStorage.removeItem('Key');"
    driver.execute_script(script_remove)

    # removal check
    value_after_remove = driver.execute_script(script_get)
    print("Value after remove:", value_after_remove)
except Exception as err:
    print(f"Error: ", err)

finally:
    driver.quit()

    