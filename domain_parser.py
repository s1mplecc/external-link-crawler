import ssl
from urllib import request
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests_html import HTMLSession


def _fetch_html(url, decode='UTF-8'):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    # ignore ssl certificate, using `ssl._create_unverified_context()`
    with request.urlopen(req, context=(ssl.SSLContext())) as res:
        return res.read().decode(decode)


def _extract_links(soup, tag='a', attr='href'):
    links = []
    for link in soup.find_all(tag):
        try:
            links.append(link[attr])
        except KeyError:  # tag not have attr
            pass
    return links


def _parse_hrefs(soup):
    return _extract_links(soup, 'a', 'href')


def _parse_img_srcs(soup):
    return _extract_links(soup, 'img', 'src')


def _parse_css_scripts(soup):
    css = _extract_links(soup, 'link', 'href')
    script = _extract_links(soup, 'script', 'src')
    return css + script


def _sort_and_deduplicate(links):
    urls = [f'{urlparse(_).scheme}://{urlparse(_).netloc}' for _ in links if 'http' in _]
    return sorted(list(set(filter(lambda _: 'http' in _, urls))))


def _parse_domains_by_requests_html(url):
    r = HTMLSession().get(url)
    absolute_links = r.html.absolute_links
    return list(set([f'{urlparse(_).scheme}://{urlparse(_).netloc}' for _ in absolute_links]))


def _merge_with_requests_html_parser(url, domains):
    url_domains = _parse_domains_by_requests_html(url) + domains
    return _sort_and_deduplicate(url_domains)


def parse_domains(url):
    soup = BeautifulSoup(_fetch_html(url), 'html.parser')

    href_domains = _merge_with_requests_html_parser(url, _parse_hrefs(soup))
    img_domains = _sort_and_deduplicate(_parse_img_srcs(soup))
    css_scripts_domains = _sort_and_deduplicate(_parse_css_scripts(soup))

    return {
        'total_domains_size': len(href_domains) + len(img_domains) + len(css_scripts_domains),
        'href_domains': href_domains,
        'href_domains_size': len(href_domains),
        'img_domains': img_domains,
        'img_domains_size': len(img_domains),
        'css_scripts_domains': css_scripts_domains,
        'css_scripts_domains_size': len(css_scripts_domains),
    }
