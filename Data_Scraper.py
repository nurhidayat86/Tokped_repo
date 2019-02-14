from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

def find(driver):
    try:
        element = driver.find_element_by_tag_name('a')
        return element
    except:
        return False


if __name__ == "__main__":

    url_path = "H:\\web_srap\\Tokopedia\\result\\link_name_ikan.csv"
    result_path = "H:\\web_srap\\Tokopedia\\result\\link_name_result_ikan.csv"

    pd_link = pd.read_csv(url_path)
    http = urllib3.PoolManager()

    title = []
    price = []
    location = []
    berat = []
    summary = []
    penjual = []
    trans_rate = []
    trans_num = []
    link = []

    for pd_idx in range(0, len(pd_link)):

        print(f"url: {pd_idx}")
        link_T = pd_link["urls"].iloc[pd_idx]
        r = http.request('GET', link_T)
        doc = r.data
        # print(doc)
        try:
            soup = BeautifulSoup(doc)
            price_T = int(str(soup.find(attrs={"class": "rvm-price mr-15"}).
                         find(attrs={"itemprop":"price"}).text).replace('.',""))
            price.append(price_T)
            title_T = str(soup.find(attrs={"class": "rvm-product-title"}).text).replace('\n',"")
            title.append(title_T)
            location_T = str(soup.find(attrs={"class": "rvm-merchat-city mt-10"}).
                            find(attrs={"class": "inline-block va-middle"}).text).replace('\n',"")
            location.append(location_T)
            berat_T = int(str(soup.find(attrs={"class": "rvm-shipping--weight"}).
                         find(attrs={"class":"rvm-shipping-content"}).text).replace('\n',"").replace(' ',"")
                         .replace('.',"").replace('gr',"").replace('kg',"000"))
            berat.append(berat_T)
            summary_T = str(soup.find(attrs={"class": "tab-content product-summary__content-box mb-30"}).
                           find(attrs={"class": "tab-pane fade product-summary__content in active"}).text)\
                .replace('\n',"").replace("                                ","")
            summary.append(summary_T)
            penjual_T = str(soup.find(attrs={"class": "rvm-merchat-name"}).
                           find(attrs={"id": "shop-name-info"}).text)
            penjual.append(penjual_T)
            trans_raw = str(soup.find(attrs={"class": "rvm-merchant-transaction"})
                            .find(attrs={"class": "description"}).text)\
                .replace('\n', "").replace("    ", "").replace("(", "").replace(")", "").split(sep=' ')
            trans_rate_T = int(trans_raw[0].replace("%",""))/100
            trans_rate.append(trans_rate_T)
            trans_num_T = trans_raw[1]
            trans_num.append(trans_num_T)
            link.append(link_T)
            print(f"title:{title_T}, price: {price_T}, location: {location_T},"
                  f"berat: {berat_T}, summary: {summary_T}, penjual: {penjual_T}, "
                  f"trans_rate: {trans_rate_T}, trans_num: {trans_num_T}, link: {link_T}")
        except:
            continue

    title = np.array(title).reshape(len(title),1)
    price = np.array(price).reshape(len(price), 1)
    location = np.array(location).reshape(len(location), 1)
    berat = np.array(berat).reshape(len(berat), 1)
    summary = np.array(summary).reshape(len(summary), 1)
    penjual = np.array(penjual).reshape(len(penjual), 1)
    trans_rate = np.array(trans_rate).reshape(len(trans_rate), 1)
    trans_num = np.array(trans_num).reshape(len(trans_num), 1)
    link = np.array(link).reshape(len(link), 1)

    data = np.concatenate((title, price, location, berat, summary, penjual, trans_rate, trans_num, link), axis=1)
    columns = ["title", "price", "location", "berat", "summary", "penjual", "trans_rate", "trans_num", "link"]

    pd_print = pd.DataFrame(columns=columns, data=data)
    print(f"berat: {pd_print}")
    pd_print.to_csv(result_path)






