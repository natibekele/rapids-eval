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

def write_who_scored_data(table,filename,index):
    data = []
    # find headers
    headers_ = table.find('thead').find('tr')
    ths_ = headers_.find_all('th')
    header_row = ['Age','Position']
    for th in ths_:
        if 'grid-ghost-cell' in th.get('class', []):
            header_row.append(th.text.strip())
        elif th.has_attr('data-stat-name'):
            header_row.append(th.text.strip())
    data.append(header_row)


    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        row_data = []
        cells = row.find_all('td')
        for cell in cells:
            if 'grid-abs' in cell.get('class', []):
                spans = cell.find_all('span')
                for s in spans:
                    if 'player-meta-data' in s.get('class', []):
                        # Split by comma or spaces, remove empty parts, then re-join with '/'
                        items = [item.strip() for item in s.text.strip().split(",") if item.strip()]
                        # Optional: if items have spaces inside but should be together, adjust splitting accordingly
                        text = "/".join(items)
                        row_data.append(text)
                        # text = s.text.strip().replace(",", '/').strip().replace(" ", "")
                        # row_data.append(text)


            elif 'grid-ghost-cell' in cell.get('class', []):
                text = cell.find('a').text
                row_data.append(text)
            else:
                row_data.append(cell.text)
        data.append(row_data)

    with open(f'{filename}-{index}.csv', 'w') as f:
        for row in data:
            f.write(','.join(row) + '\n')

# Rapids 23,24 player ratings
# url = "https://www.whoscored.com/teams/1120/archive/usa-colorado-rapids?stageId=23794"
# url = "https://www.whoscored.com/teams/1120/archive/usa-colorado-rapids?stageId=21622"

# ATL 23,24
# url = "https://www.whoscored.com/teams/26666/archive/usa-atlanta-united?stageId=22666"
# url = "https://www.whoscored.com/teams/26666/archive/usa-atlanta-united?stageId=23794"

#AUS 23,24
url = "https://www.whoscored.com/teams/29664/archive/usa-austin-fc?stageId=21622"

def scrape_page(url, key):
    print("getting page with playwright")
    html = get_page_with_playwright(url)

    print("starting parse")
    soup = BeautifulSoup(html, 'html.parser')

    print("finding tables")
    tables = soup.find_all('table')
    for i,table in enumerate(tables):
        if table.has_attr('class'):
            # write_data(table, i)
            write_who_scored_data(table, key, i)

all_urls = [
    # # {"key": "austin-23", "url": "https://www.whoscored.com/teams/29664/archive/usa-austin-fc?stageId=21622"},
    # {"key": "austin-24", "url": "https://www.whoscored.com/teams/29664/archive/usa-austin-fc?stageId=22796"},
    # {"key":"montreal-23", "url": "https://www.whoscored.com/teams/11135/archive/canada-cf-montreal?stageId=21622"},
    # {"key":"montreal-24", "url": "https://www.whoscored.com/teams/11135/archive/canada-cf-montreal"},
    # {"key":"charlotte-23", "url": "https://www.whoscored.com/teams/30105/archive/usa-charlotte-fc?stageId=22666"},
    # {"key":"charlotte-24", "url": "https://www.whoscored.com/teams/30105/archive/usa-charlotte-fc"},
    # {"key":"chicago-24", "url": "https://www.whoscored.com/teams/1118/archive/usa-chicago-fire-fc"},
    # {"key":"chicago-23", "url": "https://www.whoscored.com/teams/1118/archive/usa-chicago-fire-fc?stageId=21622"},
    # {"key":"columbus-24", "url": "https://www.whoscored.com/teams/1113/archive/usa-columbus-crew"},
    # {"key":"columbs-23", "url": "https://www.whoscored.com/teams/1113/archive/usa-columbus-crew?stageId=22666"},
    # {"key":"dc-24", "url": "https://www.whoscored.com/teams/1119/archive/usa-dc-united"},
    # {"key":"dc-23", "url": "https://www.whoscored.com/teams/1119/archive/usa-dc-united?stageId=21622"},
    # {"key":"cincinnati-24", "url": "https://www.whoscored.com/teams/24949/archive/usa-fc-cincinnati"},
    # {"key":"cincinatti-23", "url": "https://www.whoscored.com/teams/24949/archive/usa-fc-cincinnati?stageId=22666"},
    # {"key":"dallas-24", "url": "https://www.whoscored.com/teams/2948/archive/usa-fc-dallas"},
    # {"key":"dallas-23", "url": "https://www.whoscored.com/teams/2948/archive/usa-fc-dallas?stageId=22666"},
    # {"key":"houston-24", "url": "https://www.whoscored.com/teams/3624/archive/usa-houston-dynamo-fc"},
    # {"key":"houston-23", "url": "https://www.whoscored.com/teams/3624/archive/usa-houston-dynamo-fc?stageId=22666"},
    # {"key":"miami-24", "url": "https://www.whoscored.com/teams/28925/archive/usa-inter-miami-cf"},
    # {"key":"miami-23", "url": "https://www.whoscored.com/teams/28925/archive/usa-inter-miami-cf?stageId=21622"},
    # {"key":"la-galaxy-24", "url": "https://www.whoscored.com/teams/1117/archive/usa-la-galaxy"},
    # {"key":"la-galaxy-23", "url": "https://www.whoscored.com/teams/1117/archive/usa-la-galaxy?stageId=21622"},
    # {"key":"lafc-24", "url": "https://www.whoscored.com/teams/27482/archive/usa-los-angeles-fc"},
    # {"key":"lafc-23", "url": "https://www.whoscored.com/teams/27482/archive/usa-los-angeles-fc?stageId=22666"},
    # {"key":"minnesota-24", "url": "https://www.whoscored.com/teams/9293/archive/usa-minnesota-united"},
    # {"key":"minnesota-23", "url": "https://www.whoscored.com/teams/9293/archive/usa-minnesota-united?stageId=21622"},
    # {"key":"nashville-24", "url": "https://www.whoscored.com/teams/27497/archive/usa-nashville-sc"},
    # {"key":"nashville-23", "url": "https://www.whoscored.com/teams/27497/archive/usa-nashville-sc?stageId=22666"},
    # {"key":"new-england-24", "url": "https://www.whoscored.com/teams/1114/archive/usa-new-england-revolution"},
    # {"key":"new-england-23", "url": "https://www.whoscored.com/teams/1114/archive/usa-new-england-revolution?stageId=22666"},
    # {"key":"nyc-fc-24", "url": "https://www.whoscored.com/teams/19584/archive/usa-new-york-city-fc"},
    # {"key":"nyc-fc-23", "url": "https://www.whoscored.com/teams/19584/archive/usa-new-york-city-fc?stageId=21622"},
    # {"key":"ny-red-bulls-24", "url": "https://www.whoscored.com/teams/1121/archive/usa-new-york-red-bulls"},
    # {"key":"ny-red-bulls-23", "url": "https://www.whoscored.com/teams/1121/archive/usa-new-york-red-bulls?stageId=22666"},
    # {"key":"orlando-24", "url": "https://www.whoscored.com/teams/10221/archive/usa-orlando-city"},
    # {"key":"orlando-23", "url": "https://www.whoscored.com/teams/10221/archive/usa-orlando-city?stageId=22666"},
    # {"key":"philadelphia-24", "url": "https://www.whoscored.com/teams/8586/archive/usa-philadelphia-union"},
    # {"key":"philadelphia-23", "url": "https://www.whoscored.com/teams/8586/archive/usa-philadelphia-union?stageId=22666"},
    # {"key":"portland-24", "url": "https://www.whoscored.com/teams/11133/archive/usa-portland-timbers"},
    # {"key":"portland-23", "url": "https://www.whoscored.com/teams/11133/archive/usa-portland-timbers?stageId=21622"},
    # {"key":"salt-lake-24", "url": "https://www.whoscored.com/teams/2947/archive/usa-real-salt-lake"},
    # {"key":"salt-lake-23", "url": "https://www.whoscored.com/teams/2947/archive/usa-real-salt-lake?stageId=22666"},
    # {"key":"san-jose-24", "url": "https://www.whoscored.com/teams/1122/archive/usa-san-jose-earthquakes"},
    # {"key":"san-jose-23", "url": "https://www.whoscored.com/teams/1122/archive/usa-san-jose-earthquakes?stageId=22666"},
    # {"key":"seattle-24", "url": "https://www.whoscored.com/teams/5973/archive/usa-seattle-sounders-fc"},
    # {"key":"seattle-23", "url": "https://www.whoscored.com/teams/5973/archive/usa-seattle-sounders-fc?stageId=22666"},
    # {"key":"kansas-city-24", "url": "https://www.whoscored.com/teams/1116/archive/usa-sporting-kansas-city"},
    # {"key":"kansas-city-23", "url": "https://www.whoscored.com/teams/1116/archive/usa-sporting-kansas-city?stageId=22666"},
    # {"key":"st-louis-23", "url": "https://www.whoscored.com/teams/30664/archive/usa-st-louis-city?stageId=22666"},
    # {"key":"st-louis-24", "url": "https://www.whoscored.com/teams/30664/archive/usa-st-louis-city?stageId=22796"},
    # {"key":"toronto-24", "url": "https://www.whoscored.com/teams/30664/archive/usa-st-louis-city?stageId=22796"},
    # {"key":"toronto-23", "url": "https://www.whoscored.com/teams/4186/archive/canada-toronto-fc?stageId=21622"},
    # {"key":"vancouver-24", "url": "https://www.whoscored.com/teams/11134/archive/canada-vancouver-whitecaps"},
    # {"key":"vancouver-23", "url": "https://www.whoscored.com/teams/11134/archive/canada-vancouver-whitecaps?stageId=22666"},
    {"key": "atlanta-24", "url": "https://www.whoscored.com/teams/26666/archive/usa-atlanta-united"},
    {"key": "atlanta-23", "url": "https://www.whoscored.com/teams/26666/archive/usa-atlanta-united?stageId=22666"},
    {"key": "colorado-24", "url": "https://www.whoscored.com/teams/1120/archive/usa-colorado-rapids?stageId=23794"},
    {"key": "colorado-23", "url": "https://www.whoscored.com/teams/1120/archive/usa-colorado-rapids?stageId=21622"}
]


for obj in all_urls:
    key, url = obj["key"], obj["url"]
    scrape_page(url, "whoscored_2/"+key)
