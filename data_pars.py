import json
import tkinter
import time
from tkinter import ttk, SINGLE, END

from selenium.webdriver.common.by import By

# from selenium.webdriver.common.by import By

from category import PRODUCTS

from selenium import webdriver

from selenium_stealth import stealth








root = tkinter.Tk()
root.title("СберМегаМаркет")


"""Начало Виджета работы со списком товаров"""
mobile = tkinter.StringVar()
mobile_chosen = ttk.Combobox(root, width=12,state='readonly')
mobile_chosen['values'] = sorted(list(PRODUCTS.keys()))
mobile_chosen.grid(column=0, row=1, ipadx=70, ipady=6, padx=5, pady=5)
mobile_chosen.current(1)

def  submit_button_selection():
    key1 = mobile_chosen.get()
    link = f'https://www.wildberries.ru/catalog/{PRODUCTS[key1]}'
    # print(link)
    return link

label = ttk.Label(text="Выберите категорию:")
label.grid(column=0, row=0)
action = ttk.Button(root, text="Выбрать", command=submit_button_selection)
action.grid(column=0, row=2, ipadx=70, ipady=6, padx=5, pady=5)
"""Конец Виджета работы с телефонами"""


"""Начало Виджета работы с Выбором процента"""
label = ttk.Label(text="Кол-во страниц для парса:")
label.grid(column=1, row=0)
percent = [2, 5, 10, 15, 20, 25, 30]
percent_var = tkinter.StringVar(value=percent[0])


def submit_cnt():
     selection = combobox.get()
     # print(selection)
     return selection


combobox = ttk.Combobox(values=percent, textvariable=percent_var)
combobox.grid(column=1, row=1, ipadx=70, ipady=6, padx=5, pady=5)
action = ttk.Button(root, text="Выбрать", command=submit_cnt)
action.grid(column=1, row=2, ipadx=70, ipady=6, padx=5, pady=5)

"""Конец Виджета работы с Выбором процента"""

'''Логика скрипта'''


def parse_bonus():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    data = {}

    cnt = int(submit_cnt())

    for page in range(1, cnt + 1):

        try:
            url = f'{submit_button_selection()}?sort=popular&page={page}'

            driver.get(url)
            time.sleep(10)

            block = driver.find_element(By.CLASS_NAME, 'product-card-list')
            posts = block.find_elements(By.CLASS_NAME, 'product-card')
            for p in posts:
                link_class = p.find_element(By.CLASS_NAME, 'product-card__link')
                link = link_class.get_attribute('href')
                name = link_class.get_attribute('aria-label')
                sale = p.find_element(By.CLASS_NAME, 'product-card__tip').text
                price = p.find_element(By.CLASS_NAME, 'price__lower-price').text.replace(' ', '')
                rating = p.find_element(By.CLASS_NAME, 'address-rate-mini').text
                id_for_link = p.get_attribute('data-nm-id')

                data[name] = {
                    'link': link,
                    'Цена': price,
                    'Скидка_продовца': sale,
                    'Рейтинг': rating,

                }
        except:
            print('Неизвестная ошибка')

            # Открываем запись и парсим данные
    for post_url in data.values():
        driver.get(post_url['link'])
        print(f'Обрабатываем: {post_url["link"]}')
        time.sleep(9)
        try:
            price_history = driver.find_element(By.CLASS_NAME, 'price-history__trend').get_attribute('textContent')
            post_url['Изменение в цене'] = price_history
            post_url['Изменение в цене редактированное'] = price_history.replace(' ', 'P').lstrip().rstrip()
        except:
            post_url['Изменение в цене'] = 0

        with open('good_result.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    driver.quit()
"""Конец логики скрипта"""

"""Кнопка старт"""
action = ttk.Button(root, text="Запустить скрипт", command=lambda: parse_bonus())
action.grid(column=0, row=4, columnspan=4, ipadx=70, ipady=6, padx=5, pady=5)
"""Конец кнопка старт"""

root.mainloop()