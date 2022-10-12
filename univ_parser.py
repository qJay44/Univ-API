from bs4 import BeautifulSoup
from selenium import webdriver
from werkzeug.exceptions import RequestTimeout
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as rq


class UnivParser:

    def getWebData(self):
        """

        forms[0] = Очная
        forms[1] = Заочная
        forms[2] = Очно-заочная

        """
        forms = [
            '\u041e\u0447\u043d\u0430\u044f',
            '\u0417\u0430\u043e\u0447\u043d\u0430\u044f',
            '\u041e\u0447\u043d\u043e-\u0437\u0430\u043e\u0447\u043d\u0430\u044f'
        ]
        url = 'https://www.muiv.ru/studentu/fakultety-i-kafedry/fakultet-it/raspisaniya/'

        source = self.__tryToLoadPage(url)
        soup = BeautifulSoup(source, 'lxml')
        files_div = soup.find('div', class_='m-intext-docs')
        items_dict = {}

        for item in files_div.find_all('div', class_='m-doc'):
            file_props = [p for p in item.find_all('p')]
            url = file_props[0].a['href']
            url_items = url.split('/')
            fileTitle = file_props[0].a.text
            file_id = url_items[3]
            eduForm = [f for f in forms if f in fileTitle][0]
            items_dict[file_id] = {
                'eduForm': eduForm,
                'url': f'https://www.muiv.ru{url}',
                'fileID': file_id,
                'fileName': url_items[4],
                'fileSize': file_props[1].text.split(' ')[1],
                'updateTime': file_props[2].text[-10:],
                'fileTitle': fileTitle,
            }

        return items_dict

    def __tryToLoadPage(self, url):
        url_request = rq.get(url).text
        if 'https://static.stormwall.pro/ajax-loader.gif' in url_request:
            try:
                options = Options()
                options.headless = True
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'm-intext-docs')))
            except TimeoutException:
                raise RequestTimeout()
            finally:
                return driver.page_source

        return url_request

