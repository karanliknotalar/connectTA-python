import math
import re
import time

import requests
from bs4 import BeautifulSoup


class ConnectTA:
    SERIES = "series"
    MOVIES = "movies"

    def __init__(self):
        self.data = None
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
        }
        self.login_url = "https://turkcealtyazi.org/login.php"
        self.login_cookies = None
        self.login_is_ok = False
        self.per_page_content = None
        self.per_page_item_count = 28
        self.movies_list = []
        self.series_list = []
        self.counter = 0
        self.username = None

    def login(self, username, password):
        if not self.login_is_ok:
            self.data = {
                "redirect": "/index.php",
                "username": username,
                "password": password,
                "login": "Giriş"
            }

            response = requests.post(self.login_url, data=self.data, headers=self.header)

            if response.status_code == 200:
                if username in response.content.decode():
                    self.login_cookies = response.cookies
                    self.login_is_ok = True
                    self.username = username
                    print("Login is successful")
            else:
                print("Login failed", response.status_code)
        else:
            print("Already Signed In")

    def get_series_list(self, startPage):
        response = requests.get(f"https://turkcealtyazi.org/watch.php?is=slist&p={startPage}",
                                cookies=self.login_cookies,
                                headers=self.header)

        if response.status_code == 200:
            self.get_per_page_items(response.content.decode(), startPage, tp=self.SERIES)

    def get_movies_list(self, startPage):
        response = requests.get(f"https://turkcealtyazi.org/watch.php?is=list&p={startPage}",
                                cookies=self.login_cookies,
                                headers=self.header)

        if response.status_code == 200:
            self.get_per_page_items(response.content.decode(), startPage, tp=self.MOVIES)

    def get_per_page_items(self, page_content, start_page, tp):
        soup = BeautifulSoup(page_content, 'html.parser')
        title = soup.find("td", attrs={"height": "30", "style": "padding:4px;"}).get_text()
        total_item_count = int(re.search("(\d+)", title).group(1))
        total_page_count = math.ceil(total_item_count / self.per_page_item_count)

        elements = soup.find("div", attrs={"class": "nblock"}).find("ul").find_all("li")

        for e in elements:
            movie_imdb = e.find_next("div", attrs={"class": "ncorner"}).get_text().strip()
            movie_name = e.find_next("span").get_text().strip()
            movie_image = e.find_next("img", attrs={"alt": e.find_next("span").get_text().strip()})["src"]
            movie_url = e.find_next("a", attrs={"title": e.find_next("span").get_text().strip()})["href"]
            if tp == self.SERIES:
                self.series_list.append({"movie_imdb": movie_imdb, "movie_name": movie_name,
                                         "movie_image": f"https://turkcealtyazi.org{movie_image}",
                                         "movie_url": f"https://turkcealtyazi.org{movie_url}"})
            if tp == self.MOVIES:
                self.movies_list.append({"movie_imdb": movie_imdb, "movie_name": movie_name,
                                         "movie_image": f"https://turkcealtyazi.org{movie_image}",
                                         "movie_url": f"https://turkcealtyazi.org{movie_url}"})
        self.counter += len(elements)

        print(f"\rListelenen: {self.counter} | Tamamlanan: {math.ceil((self.counter / total_item_count) * 100)}%\r",
              end="")
        time.sleep(1)
        if total_page_count != start_page:
            time.sleep(1)

            if tp == self.SERIES:
                self.get_series_list(start_page + 1)
            if tp == self.MOVIES:
                self.get_movies_list(start_page + 1)
        else:
            print("\nTüm liste alındı:", self.counter)

    def reset_list(self, tp):
        self.counter = 0
        if tp == self.MOVIES:
            self.movies_list = []
        if tp == self.SERIES:
            self.series_list = []
