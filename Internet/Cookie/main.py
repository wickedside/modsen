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

    # set value in Cookie
    driver.add_cookie({'name': 'Cookieeee:)', 'value': 'someCookieVal'})

    # get value from Cookie
    cookie = driver.get_cookie('Cookieeee:)')
    print("Cookie value:", cookie)

    # remove value from Cookie
    driver.delete_cookie('Cookieeee:)')

    # removal check
    cookie_after_remove = driver.get_cookie('Cookieeee:)')
    print("Cookie value after remove:", cookie_after_remove)
except Exception as err:
    print(f"Error: ", err)

finally:
    driver.quit()


