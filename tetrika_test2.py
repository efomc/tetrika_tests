from bs4 import BeautifulSoup
import requests
import re


def get_soup(url):
    requests.get(url)
    pages = requests.get(url)
    return BeautifulSoup(pages.text, "lxml")


def get_animal_in_page(soup):
    span_animal = soup.find_all("div", class_="mw-category mw-category-columns")
    animal_raw = "".join([item.text for item in span_animal])
    return set(
        item
        for item in animal_raw.split("\n")
        if len(item) > 1 and item[0] in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
    )


def get_next_page_url(soup):
    span_next_page = soup.find_all(title="Категория:Животные по алфавиту")
    link_item = [
        str(item) for item in span_next_page if item.text == "Следующая страница"
    ][0]
    link_item = re.findall(r'href="[\S]+"', link_item)[0]
    link_item = link_item.replace('href="', "").replace('"', "").replace("amp;", "")
    return "https://ru.wikipedia.org" + link_item


def main():
    animal_set = set()

    url = "https://inlnk.ru/jElywR"

    soup = get_soup(url)
    addition_animal_set = get_animal_in_page(soup)

    while addition_animal_set:
        animal_set.update(addition_animal_set)

        next_url = get_next_page_url(soup)
        soup = get_soup(next_url)
        addition_animal_set = get_animal_in_page(soup)

    result_dict = {
        letter: len([item for item in animal_set if item.startswith(letter)])
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"
    }
    for key in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ":
        print(f"{key}: {result_dict[key]}")


if __name__ == "__main__":
    main()
