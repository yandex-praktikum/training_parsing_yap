from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

WHATS_NEW_URL = 'https://docs.python.org/3.14/whatsnew/'

if __name__ == '__main__':
    session = requests_cache.CachedSession()
    response = session.get(WHATS_NEW_URL, timeout=10)
    response.raise_for_status()
    response.encoding = 'utf-8'
    if not response.text.strip():
        raise ValueError('Получена пустая страница нововведений')
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = soup.find('section', id='what-s-new-in-python')
    if main_div is None:
        raise ValueError('Не найден раздел нововведений')
    div_with_ul = main_div.find('div', class_='toctree-wrapper')
    if div_with_ul is None:
        raise ValueError('Не найден список статей')
    sections_by_python = div_with_ul.find_all('li', class_='toctree-l1')
    if not sections_by_python:
        raise ValueError('Список статей пуст')
    index_url = response.url
    results = []
    for section in tqdm(sections_by_python, desc='Статьи о нововведениях'):
        version_a_tag = section.find('a')
        if version_a_tag is None or not version_a_tag.get('href'):
            raise ValueError('В элементе списка нет ссылки')
        href = version_a_tag['href']
        # Changelog — журнал изменений, а не статья о новой версии.
        if href == 'changelog.html':
            continue
        version_link = urljoin(index_url, href)
        article_response = session.get(version_link, timeout=10)
        article_response.raise_for_status()
        article_response.encoding = 'utf-8'
        if not article_response.text.strip():
            raise ValueError(f'Получена пустая статья: {version_link}')
        article_soup = BeautifulSoup(article_response.text, features='lxml')
        h1 = article_soup.find('h1')
        if h1 is None:
            raise ValueError(f'Не найден заголовок статьи: {version_link}')
        title = h1.get_text(' ', strip=True).removesuffix('¶').strip()
        if not title:
            raise ValueError(f'Заголовок статьи пуст: {version_link}')
        metadata = article_soup.find('dl', class_='field-list')
        authors = []
        if metadata is not None:
            for field in metadata.find_all('dt'):
                label = field.get_text(' ', strip=True).rstrip(':').strip()
                if label in ('Author', 'Authors', 'Editor', 'Editors'):
                    value = field.find_next_sibling('dd')
                    if value is None or not value.get_text(strip=True):
                        raise ValueError(f'Поле автора пусто: {version_link}')
                    authors.append(value.get_text(' ', strip=True))
        author_text = '; '.join(authors) if authors else 'Автор не указан'
        results.append((version_link, title, author_text))
    if not results:
        raise ValueError('Не собрано ни одной статьи')
    for row in results:
        print(*row)
