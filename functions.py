from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import join
from time import sleep


def get_category(driver):
    categories = list()
    categories_div = '//div[@id="collapse-categorias"]'
    categories_a = '//a[@class="filter-list-link filter-show-result filter-list-link-basic filter-hide-count"]'
    seemore_button = '//button[@class="btn-seemore-filter btn btn-xs btn-link btn-block"]'
    try:
        button = driver.find_element_by_xpath(categories_div+seemore_button)
        button.click()
    except (NoSuchElementException, ElementNotInteractableException):
        pass
    try:
        elements = driver.find_elements_by_xpath(categories_div+categories_a)
        for element in elements:
            link = element.get_attribute('href')
            name = element.get_attribute('innerHTML')
            name = name.replace('<span>', '').replace('</span>', '')
            info = (link, name)
            categories.append(info)
    except NoSuchElementException:
        info = (driver.current_url, 'None')
        categories.append(info)

    print(len(categories))
    return categories


def get_pagination(driver):
    links = set()
    try:
        pagination = driver.find_element_by_xpath(
            '//ul[@class="pagination-product-grid pagination"]')
        link_elements = pagination.find_elements_by_css_selector('a')
        for element in link_elements:
            links.add(element.get_attribute('href'))
        if len(links) == 0:
            links.add(driver.current_url)
    except NoSuchElementException:
        links.add(driver.current_url)
    print(len(links))
    return links


def get_book_info(driver):
    books = list()
    shelf_div = '//div[@class="row product-grid no-gutters main-grid"]'
    clicable_div = '//div[@class="RippleContainer-sc-1rpenp9-0 dMCfqq"]'
    link_a = '//a[@class="Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc"]'
    title_h2 = '//h2[@class="TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 fINzxm"]'
    price_span = '//span[@class="PriceUI-bwhjk3-11 jtJOff PriceUI-sc-1q8ynzz-0 inNBs TextUI-sc-12tokcy-0 CIZtP"]'
    check = True
    refreshes = 0
    while check:
        try:
            link_elements = driver.find_elements_by_xpath(shelf_div+clicable_div+link_a)
            title_elements = driver.find_elements_by_xpath(shelf_div+title_h2)
            price_elements = driver.find_elements_by_xpath(shelf_div+price_span)
            elements = zip(link_elements, title_elements, price_elements)
            for raw_link, raw_title, raw_price in elements:

                link = raw_link.get_attribute('href')
                title = raw_title.get_attribute('innerHTML')
                price = raw_price.get_attribute('innerHTML').replace('R$ <!-- -->', '')
                price = price.replace(',', '.')
                info = (link, title, price)
                books.append(info)
            check = False
        except StaleElementReferenceException:
            if refreshes > 1:
                print('StaleElementReferenceException', driver.current_url)
                check = False
            else:
                driver.refresh()
                refreshes += 1
                check = True
        if len(link_elements) == 0 and refreshes == 0:
            refreshes += 1
            check = True
    return books
