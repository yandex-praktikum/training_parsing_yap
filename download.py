import re
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from zipfile import is_zipfile

import requests_cache
from bs4 import BeautifulSoup

DOWNLOADS_URL = 'https://docs.python.org/3.14/download.html'
BASE_DIR = Path(__file__).resolve().parent

if __name__ == '__main__':
    session = requests_cache.CachedSession()
    response = session.get(DOWNLOADS_URL, timeout=10)
    response.raise_for_status()
    response.encoding = 'utf-8'
    if not response.text.strip():
        raise ValueError('Получена пустая страница загрузок')
    soup = BeautifulSoup(response.text, features='lxml')
    main_tag = soup.find('div', role='main')
    if main_tag is None:
        raise ValueError('Не найден основной раздел страницы загрузок')
    table_tag = main_tag.find('table', class_='docutils')
    if table_tag is None:
        raise ValueError('Не найдена таблица архивов')
    html_tag = table_tag.find('a', href=re.compile(r'.+docs-html\.zip$'))
    if html_tag is None:
        raise ValueError('Не найдена ссылка на HTML ZIP')
    archive_url = urljoin(response.url, html_tag['href'])
    filename = urlsplit(archive_url).path.split('/')[-1]
    archive_response = session.get(archive_url, timeout=30)
    archive_response.raise_for_status()
    if not archive_response.content or not is_zipfile(BytesIO(archive_response.content)):
        raise ValueError('Вместо ZIP получен пустой или другой ответ')
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    with open(archive_path, 'wb') as file:
        file.write(archive_response.content)
    print('Архив сохранён:', archive_path)
