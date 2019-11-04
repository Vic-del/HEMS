from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json
import pandas as pd

pricesList = []
namePhone = []

try:
    html = urlopen("https://www.antutu.com/en/ranking/rank1.html")

except HTTPError as e:
    print(e)

except URLError:
    print("Server down or incorrect domain")

else:
    direction = BeautifulSoup(html.read(), "html5lib")
    nameTags = direction.findAll("div", {"class": "rank_left"})
    browser = webdriver.Chrome('C://Users//Eztena//.wdm//chromedriver//75.0.3770.140//win32//chromedriver.exe')
    timeout = 20

    try:
        WebDriverWait(browser, timeout)

    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    for tag in nameTags:
        phone = tag.getText()
        firstSplit = phone.split('(')[0]
        namePhone.append(firstSplit)
        address = 'https://google.com/search?q=' + '"' + firstSplit + '"' + '&source=lnms&tbm=shop&sa=X&ved=0ahUKEw'
        browser.get(address)

        # find_elements_by_xpath returns an array of selenium objects.
        prices_element = browser.find_elements_by_xpath("//span[@class='O8U6h']")
        prices = [float(''.join(filter(str.isdigit, x.text))) for x in prices_element]
        adjustPrices = list(filter(lambda x: x > 10000, prices))

        try:
            averagePrice = sum(adjustPrices) / (len(adjustPrices) * 100)
            pricesList.append(averagePrice)
            print(averagePrice)

        except ZeroDivisionError:

            print("precio no disponible")

        print()

Data = {
    'Modelo': namePhone,
    'Precio medio': pricesList
}

df = pd.DataFrame(Data, columns=['Modelo', 'Precio medio'])
df = df.to_json()

with open('df.json', 'w') as f:
    json.dump(df, f)
