import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup

PYTHON_DOWNLOADS_URL = 'https://www.python.org/downloads/'

if __name__ == '__main__':
    session = requests_cache.CachedSession()
    response = session.get(PYTHON_DOWNLOADS_URL, timeout=10)
    response.raise_for_status()
    response.encoding = 'utf-8'
    if not response.text.strip():
        raise ValueError('Получена пустая страница версий')
    soup = BeautifulSoup(response.text, features='lxml')
    releases = soup.find('ol', class_='list-row-container')
    if releases is None:
        raise ValueError('Не найден список версий Python')
    rows = releases.find_all('li', recursive=False)
    if not rows:
        raise ValueError('Список версий Python пуст')
    results = []
    for row in rows:
        version_tag = row.find('span', class_='release-version')
        status_tag = row.find('span', class_='release-status')
        download_tag = row.find('span', class_='release-dl')
        if version_tag is None or status_tag is None or download_tag is None:
            raise ValueError('В строке версии отсутствует ожидаемое поле')
        version_match = re.fullmatch(r'\d+\.\d+', version_tag.get_text(strip=True))
        if version_match is None:
            raise ValueError('Не распознан номер версии Python')
        version = version_match.group()
        status = status_tag.get_text(' ', strip=True)
        a_tag = download_tag.find('a')
        if not status or a_tag is None or not a_tag.get('href'):
            raise ValueError('В строке версии нет статуса или ссылки')
        link = urljoin(response.url, a_tag['href'])
        results.append((link, version, status))
    for row in results:
        print(*row)
