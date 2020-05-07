from selenium.common.exceptions import NoSuchElementException
from os.path import join
from time import sleep


def get_category_links(driver):
    elements = driver.find_elements_by_xpath(
        '//a[@class="filter-list-link filter-show-result filter-list-link-basic filter-hide-count"]')
    links = list()
    for element in elements:
        links.append(element.get_attribute('href'))

    return links


def get_pagination_links(driver):
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
    return links


def get_books_links(driver):
    links = list()
    try:
        shelf = driver.find_element_by_xpath(
            '//div[@data-publish-name="Verticais Livros - Teste Zion Vitrine - Componente"]')
        link_elements = driver.find_elements_by_xpath('//a[@class="card-product-url"]')
        for link in link_elements:
            links.append(link.get_attribute('href'))
    except NoSuchElementException:
        try:
            shelf = driver.find_element_by_xpath(
                '//div[@class="row product-grid no-gutters main-grid"]')
            books = shelf.find_elements_by_xpath(
                '//div[@class="product-grid-item ColUI-gjy0oc-0 ifczFg ViewUI-sc-1ijittn-6 iXIDWU"]')
            for book in books:
                link_element = book.find_element_by_css_selector('a')
                links.append(link_element.get_attribute('href'))
        except NoSuchElementException:
            print(f'books not found in "{driver.current_url}"')

    return links


def get_book_info(driver):
    try:
        category_elements = driver.find_elements_by_xpath(
            '//a[@class="BreadcrumbItem-ohhfq9-1 jSVYeJ LinkUI-sc-1soz7d4-0 fQBLjw"]')
        if len(category_elements) > 0:
            category_info = (category_elements[-1].get_attribute('href'))
            category_info = category_info.split('/')[5:]
            category_info = '-'.join(category_info)
        else:
            category_info = 'None'
    except NoSuchElementException:
        category_info = 'None'

    try:
        name_element = driver.find_element_by_xpath('//h1[@id="product-name-default"]')
        name_info = name_element.get_attribute('innerHTML')
    except NoSuchElementException:
        name_info = 'None'

    try:
        driver.implicitly_wait(0.5)
        try:
            price_element = driver.find_element_by_xpath(
                '//span[@class="sales-price main-offer__SalesPrice-sc-1oo1w8r-1 fiWaea TextUI-sc-12tokcy-0 CIZtP"]')
        except NoSuchElementException:
            price_element = driver.find_element_by_xpath(
                '//span[@class="price__SalesPrice-sc-1i11rkh-2 jjADsQ TextUI-sc-12tokcy-0 CIZtP"]')
        price_info = price_element.get_attribute('innerHTML')
        price_info = price_info.replace('R$', '').strip()

    except NoSuchElementException:
        price_info = 'None'

    driver.implicitly_wait(3)
    return category_info, name_info, price_info
