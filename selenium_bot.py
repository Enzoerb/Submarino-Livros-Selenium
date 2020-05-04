from selenium import webdriver
from datetime import datetime
from functions import get_category_links, get_pagination_links, get_books_links, get_book_info
from pprint import pprint
from time import sleep

beggining = datetime.now()
with webdriver.Chrome() as driver:
    driver.implicitly_wait(3)
    driver.get("https://www.submarino.com.br/categoria/livros?chave=prf_hm_mn_bn_0_2_livros")
    with open('submarion_books.txt', 'w') as file:
        category_links = get_category_links(driver)
        for category in category_links:
            driver.get(category)
            pagination = get_pagination_links(driver)
            for page in pagination:
                driver.get(page)
                books_links = get_books_links(driver)
                file.write(f'Page: {page}\n')
                file.write(f'has {len(books_links)} books\n\n')
                for book in books_links:
                    driver.get(book)
                    category_info, name_info, price_info = get_book_info(driver)
                    file.write('category info: ')
                    file.write(f'{category_info}')
                    file.write('\n')
                    file.write('name info: ')
                    file.write(f'{name_info}')
                    file.write('\n')
                    file.write('price info: ')
                    file.write(f'{price_info}')
                    file.write('\n\n')

                file.write('\n--//--\n\n')
end = datetime.now()
time = end - beggining
print(time)
