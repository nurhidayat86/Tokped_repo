# from bs4 import BeautifulSoup
import pandas as pd
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

    # user parameter
    link_path = "H:\\web_srap\\Tokopedia\\result\\link_name_totbag.csv"

    # Tokopedia aprameters
    p_url = r'https://www.tokopedia.com/'
    str_query = "tote bag"
    str_query = str_query.replace(" ","%20")
    print(str_query)

    # URL chromedriver
    driver_p = r'C:\firefox_driver\chromedriver_win32\chromedriver.exe'
    # soup = BeautifulSoup(p_url, 'html5lib')
    # print(soup.prettify())

    driver = webdriver.Chrome(driver_p)
    driver.get(p_url)

    # Print driver title first
    title1st = driver.title

    # Look for login button and click
    elem = driver.find_element_by_id("login-ddl-link")
    elem.click()

    # handle iframe login
    wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("iframe-accounts"))
    elem = driver.find_element_by_id("inputEmail")
    elem.send_keys('youremail@mail.com')
    elem = driver.find_element_by_id("inputPassword")
    elem.send_keys('yourpassword')
    elem = driver.find_element_by_id("global_login_btn")
    elem.click()

    # go out from iframe and to tokopedia
    driver.switch_to.default_content()

    #Loop per page
    page_exist = True
    page = 1
    page_th = 50

    driver.get(f'https://www.tokopedia.com/search?st=product&q={str_query}')
    hdr_flag = True

    while(page_exist == True):
        link_name = []

        elem = driver.find_elements_by_class_name("_27sG_y4O")

        print(f"len of size in this page:{len(elem)}")

        page += 1
        for elem_size in range(0, len(elem)):
            try:
                element = wait(elem[elem_size],10).until(find)
                l_name = element.get_attribute('href')
                # driver2 = webdriver.Chrome(driver_p)
                # driver2.get(l_name)
                # driver2.close()
                link_name.append(element.get_attribute('href'))
            except:
                continue

        if hdr_flag == True:
            pd.DataFrame(columns=["urls"], data=link_name).to_csv(link_path, mode='a')
            hdr_flag = False
        else:
            pd.DataFrame(columns=["urls"], data=link_name).to_csv(link_path, mode='a', header=False)

        try:
            # Try to check if there is a next link
            driver.find_element_by_link_text(">")
            print(f"GO to page-{page}")
            driver.get(f'https://www.tokopedia.com/search?st=product&q={str_query}&page={page}')
            driver.implicitly_wait(10)
        except:
            # There is no next link
            page_exist = False

        if page > page_th:
            page_exist = False

        # page_exist = False

    link_name = np.array(link_name)
