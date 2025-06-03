import requests
from bs4 import BeautifulSoup
from playwright._impl._errors import TimeoutError
from playwright.sync_api import sync_playwright


def get_page_with_playwright(url):
    with sync_playwright() as p:
        print("launch browser")
        browser = p.chromium.launch(headless=True)
        print("launced browser")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="America/New_York"
        )

        page= context.new_page()
        try:
            page.goto(url, timeout=5000)
        except TimeoutError:
            print("timeout error, still try to proceed.")

        content = page.content()
        browser.close()
        return content

def write_data(table, index):
    data = []
    # find headers
    thead_tr = table.find('thead').find_all('tr')
    tbody_tr = table.find('tbody').find_all('tr')

    for tr in thead_tr:
        if tr.has_attr('class'):
            continue
        _row = []
        th = tr.find_all('th')
        for _th in th:
            if _th.has_attr('data-stat'):
                _row.append(_th['data-stat'])

        data.append(_row)

    for tr in tbody_tr:
        _row = []
        th = tr.find('th')
        if th.has_attr('data-stat'):
            _row.append(th.get_text())
        td = tr.find_all('td')
        for _td in td:
            if _td.has_attr('data-stat'):
                _row.append(_td.get_text().replace(',', ''))

        data.append(_row)

    with open(f'data-{index}.csv', 'w') as f:
        for row in data:
            f.write(','.join(row) + '\n')

url = "https://fbref.com/en/comps/22/2024/wages/2023-Major-League-Soccer-Wages"

print("getting page with playwright")
html = get_page_with_playwright(url)

print("starting parse")
soup = BeautifulSoup(html, 'html.parser')

print("finding tables")
tables = soup.find_all('table')
for i,table in enumerate(tables):
    if table.has_attr('class'):
        write_data(table, i)
