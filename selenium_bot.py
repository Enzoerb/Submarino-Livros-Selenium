from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from functions import get_category, get_pagination, get_book_info
from pprint import pprint
from time import sleep

beggining = datetime.now()
with webdriver.Chrome() as driver:
    driver.implicitly_wait(3)
    driver.get("https://www.submarino.com.br/categoria/livros?chave=prf_hm_mn_bn_0_2_livros")
    with open('submarion_books.csv', 'w') as file:
        category_info = get_category(driver)
        print(f'categories count: {len(category_info)}')
        for category_link, category_name in category_info:
            try:
                driver.get(category_link)
            except TimeoutException:
                break
            subcategory_info = get_category(driver)
            print(f'subcategories count: {len(subcategory_info)}')
            for subcategory_link, subcategory_name in subcategory_info:
                try:
                    driver.get(subcategory_link)
                except TimeoutException:
                    break
                print(f'{category_name} > {subcategory_name}')
                pagination = get_pagination(driver)
                print(f'pages count: {len(pagination)}')
                for page in pagination:
                    try:
                        driver.get(page)
                    except TimeoutException:
                        break
                    books = get_book_info(driver)
                    for link, title, price in books:
                        book_info = [str(category_name), str(subcategory_name),
                                     str(link), str(title), str(price)]
                        delimiter = '|'
                        file.write(f'{delimiter.join(book_info)}\n')
end = datetime.now()
time = end - beggining
print(time)
