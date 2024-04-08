from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    path_to_site = 'https://libra.ibuk.pl/ksiazki?_page=1'
    resp = requests.get(path_to_site)
    soup = BeautifulSoup(resp.text, 'html.parser')
    pages = soup.find_all('a', class_='page-link')
    max_label = None
    for page in pages:
        label = page.get('aria-label')
        if label and label.isdigit():
            label_int = int(label)
            if max_label is None or label_int > max_label:
                max_label = label_int
                
    driver = webdriver.Firefox()
    for number in range(1,max_label):
        driver.get(f'https://libra.ibuk.pl/ksiazki?_page={number}')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[_ngcontent-app-libra-2-c44]')))
        links = soup.find_all('a', attrs={'_ngcontent-app-libra-2-c44': True})
        for link in links:
            book = link['href']
            book_path = f"https://libra.ibuk.pl{book}"
            response = requests.get(book_path)
            soup2 = BeautifulSoup(response.text, 'html.parser')
            titles = soup2.find_all('h1', class_='header-size my-3')
            if titles:
                for title in titles:
                    print(title.text.strip())
            else:
                print("Brak tytułów dla danej strony")



    driver.quit()

main()