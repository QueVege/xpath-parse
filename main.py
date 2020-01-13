import lxml.html as html
import requests
import json

PAGES_COUNT = 3

page_url = "https://tproger.ru/"
output = []

for i in range(PAGES_COUNT):
    page_info = {}
    page_info['page'] = i+1
    page_info['url'] = page_url
    page_info['posts'] = []
    req = requests.get(page_url)
    page = html.fromstring(
        req.content
    )
    post_url_list = page.xpath(
        "//article/a/@href"
    )
    for post_url in post_url_list:
        post_info = {}
        post_info['url'] = post_url
        req = requests.get(post_url)
        post = html.fromstring(
            req.content
        )

        # Получить информацию(title, body, images, datePublished)
        
        title = post.xpath(
            "//h1[contains(@class, 'entry-title')]/text()"
        )
        post_info['title'] = title[0]

        created_date = post.xpath(
            "//time[contains(@class, 'entry-date')]/text()"
        )
        post_info['created_date'] = created_date[0]

        body = post.xpath(
            "//div[contains(@class, 'entry-content')]//text()"
        )
        body = list(filter(lambda e: (e != "\n" and e != " "), body))
        post_info['body'] = "\n".join(body)

        images = post.xpath(
            "//article//img/@src"
        )
        post_info['images'] = images

        page_info['posts'].append(post_info)

    output.append(page_info)

    page_url = page.xpath(
        "//a[contains(@class, 'icon-angle-right')]/@href"
    )
    if not page_url:
        break
    page_url = page_url[0]

with open('output.txt', 'w', encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
f.close()