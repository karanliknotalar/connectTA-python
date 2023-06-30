import datetime
from pathlib import Path

from bs4 import BeautifulSoup

home_dir = Path.home() / 'Desktop'


def empty(movie_url, movie_name, movie_image, movie_imdb):
    return f'''<tr class="tr">
                <td class="td2">
                    <a href="{movie_url}" title="{movie_name}">
                        <img src="{movie_image}" class="img" alt="{movie_name}">
                    </a>
                </td>
                <td class="td">
                    <a href="{movie_url}" title="{movie_name}">
                        <span class="title">{movie_name}</span>
                    </a>
                    <br>
                    <span class="puantext">IMDB: {movie_imdb}</span>
                </td>
            </tr>'''


def empty_with_db(movie_url, movie_name, movie_image, movie_imdb):
    return f'''<tr>
    <td>
        <a href="{movie_url}" title="{movie_name}">
            <img alt="{movie_name}" class="w-auto" style="width: 5rem !important;" 
            src="{movie_image}"/>
        </a>
    </td>
    <td><b>{movie_imdb}</b></td>
    <td>
        <a href="{movie_url}" title="{movie_name}"><b>{movie_name}</b></a>
    </td>
    </tr>'''


def save_html(movies, tp, mode):
    soup = None
    if mode == 1:
        soup = BeautifulSoup(open("empty.html", encoding='utf-8').read(), 'html.parser')
    if mode == 2:
        soup = BeautifulSoup(open("empty_with_db.html", encoding='utf-8').read(), 'html.parser')
    soup.find("h3").string = f"İzlediğim {tp}ler ({len(movies)} {tp}) (Eklenme Tarihine Göre Yeniden Eskiye)"
    soup.find("h5").string = datetime.datetime.now().strftime("Tarih: %d.%m.%Y Saat: %H:%M")
    selected = soup.find('tbody', {'class': 'tbody'})
    for movie in movies:
        if mode == 1:
            selected.append(
                BeautifulSoup(empty(movie["movie_url"], movie["movie_name"], movie["movie_image"], movie["movie_imdb"]),
                              'html.parser'))
        if mode == 2:
            selected.append(
                BeautifulSoup(
                    empty_with_db(movie["movie_url"], movie["movie_name"], movie["movie_image"], movie["movie_imdb"]),
                    'html.parser'))
    result = str(soup)

    with open(f'{home_dir}/{tp.lower()}_{mode}.html', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"{home_dir}/{tp.lower()}_{mode}.html dosyası kaydedildi.")


def save_txt(movies, tp):
    with open(f'{home_dir}/{tp.lower()}.txt', 'w', encoding='utf-8') as f:
        f.write(f"İzlediğim {tp}ler ({len(movies)} {tp}) (Eklenme Tarihine Göre Yeniden Eskiye)\n")
        f.write(datetime.datetime.now().strftime("Tarih: %d.%m.%Y Saat: %H:%M\n\n"))
        for movie in movies:
            f.write("-" * 80)
            f.write(f"\nFilm Adı: {movie['movie_name']}\n")
            f.write(f"Film IMDB Puanı: {movie['movie_imdb']}\n")
            f.write(f"Film Resmi: {movie['movie_image']}\n")
            f.write(f"Film Url: {movie['movie_url']}\n")
    print(f"{home_dir}/{tp.lower()}.txt dosyası kaydedildi.")
