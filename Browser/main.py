from selenium import webdriver
from selenium.webdriver.chrome.options import Options

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

options = Options()
if brave_path:
    options.binary_location = brave_path
options.add_argument("--incognito --enable-chrome-browser-cloud-management")

driver = webdriver.Chrome(options=options)
website_url = "https://thesr.live"
driver.get(website_url) #opens the main window (must)
driver.execute_script("window.open('https://thesr.live');")
driver.execute_script("window.open('');")
input("Press Enter to close the browser...") #so that  we can see the website before closing it
driver.quit() #closes all windows