from urllib.parse import unquote

import bs4
import requests


def parse(title, key):
    title = title.split()
    normalize_title = '+'.join(title)

    if key == 'f':
        url = f'https://www.movie-map.com/{normalize_title}'
    if key == 'm':
        url = f'https://www.music-map.com/{normalize_title}'

    r = requests.get(url)

    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    list_film = soup.find_all('a', class_='S')
    list_film = list(map(lambda x: x.get('href'), list_film[1:]))

    normalize_list_film = list(map(lambda x: x.replace('+', ' ') if '+' in x else x, list_film))

    normalize_list_film = list(map(lambda x: unquote(x), normalize_list_film))

    print(normalize_list_film)

    return normalize_list_film
