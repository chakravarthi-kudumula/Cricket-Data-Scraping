from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450"

options = Options()

options.add_argument("--user-data-dir=/Users/chakri/Desktop/selenium_chrome_profile")
options.add_argument("--profile-directory=Default")

options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(url)
time.sleep(10)

print("TITLE:", driver.title)
print("HTML LENGTH:", len(driver.page_source))

driver.get(url)
time.sleep(10)

print("TITLE:", driver.title)
print("HTML LENGTH:", len(driver.page_source))

input("Press Enter to close browser...")
driver.quit()