"""Check generated SEO metadata, structured data, local links, and product coverage."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET
from build import DOMAIN, ROOT

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links, self.ids, self.schemas = [], set(), []
        self.canonical, self.description, self.title = [], [], ''
        self.h1 = 0
        self.in_title = self.in_schema = False
        self.schema = ''
        self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description.append(attrs['content'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.in_title = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True
            self.schema = ''
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schema += data
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script' and self.in_schema:
            self.schemas.extend(json.loads(self.schema))
            self.in_schema = False

pages = {p: Page(p.read_text()) for p in ROOT.rglob('index.html')}
titles = set()
all_links = set()
for file, page in pages.items():
    relative = file.parent.relative_to(ROOT).as_posix()
    route = '/' if relative == '.' else '/' + relative + '/'
    assert page.canonical == [DOMAIN + route], (file, page.canonical)
    assert page.h1 == 1 and page.description and page.title, file
    assert page.title not in titles, 'Duplicate title'
    titles.add(page.title)
    for schema in page.schemas:
        assert schema['@type'] != 'Review', 'Unsupported review schema'
    if route.startswith('/articles/'):
        assert any(s['@type'] == 'BlogPosting' for s in page.schemas), file
        assert 'Ownership disclosure' in file.read_text(), file
    for link in page.links:
        all_links.add(link)
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        target = ROOT / unquote(parsed.path).lstrip('/') if parsed.path else file
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), (file, link)
        if parsed.fragment:
            target_page = pages.get(target) or Page(target.read_text())
            assert unquote(parsed.fragment) in target_page.ids, (file, link)
    assert 'spiritualai-reviews.com' not in file.read_text(), file
for product in ['https://spiritualai.xyz/', 'https://spiritualai.store/', 'https://21days.store/', 'https://aihelper.si/']:
    assert product in all_links, product
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = {item.text for item in sitemap.findall('.//{*}loc')}
assert locations == {p.canonical[0] for p in pages.values()}
assert DOMAIN + '/sitemap.xml' in (ROOT / 'robots.txt').read_text()
assert len(pages) == 13, len(pages)
print(f'PASS: {len(pages)} pages; unique titles, canonical URLs, JSON-LD, sitemap, internal links, fragments, disclosures, and all four product destinations')
