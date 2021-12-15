from urllib import request
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def _fetch_html(url, decode='UTF-8'):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    with request.urlopen(req) as res:
        return res.read().decode(decode)


def _parse_hrefs(soup):
    links = soup.find_all('a')
    hrefs = []
    for link in links:
        try:
            hrefs.append(link['href'])
        except KeyError:
            pass
    return hrefs


def _parse_img_srcs(soup):
    links = soup.find_all('img')
    imgs = []
    for link in links:
        try:
            imgs.append(link['src'])
        except KeyError:
            pass
    return imgs


def parse_domains(url):
    soup = BeautifulSoup(_fetch_html(url), 'html.parser')
    hrefs = _parse_hrefs(soup)
    img_srcs = _parse_img_srcs(soup)
    href_domains = sorted(list(set([urlparse(_).netloc for _ in hrefs if 'http' in _])))
    img_domains = sorted(list(set([urlparse(_).netloc for _ in img_srcs if 'http' in _])))
    return {
        'href_domains': href_domains,
        'href_domains_size': len(href_domains),
        'img_domains': img_domains,
        'img_domains_size': len(img_domains),
    }
