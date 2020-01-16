import lxml.html as html
import requests
import json


PAGES_COUNT = 3


def get_next_page(current_page):
    next_page_url = current_page.xpath(
        "//a[contains(@class, 'icon-angle-right')]/@href"
    )
    if next_page_url:
        return next_page_url[0]


def get_info_from_url(post_url):
    post_info = {}

    post_info['url'] = post_url

    req = requests.get(post_url)
    post = html.fromstring(req.content)

    title = post.xpath(
        "//h1[contains(@class, 'entry-title')]/text()"
    )
    if title:
        post_info['title'] = title[0]

    created_date = post.xpath(
        "//time[contains(@class, 'entry-date')]/text()"
    )
    if created_date:
        post_info['created_date'] = created_date[0]

    body = post.xpath(
        "//div[contains(@class, 'entry-content')]//text()"
    )
    body = list(filter(lambda e: (e != "\n" and e != " "), body))
    post_info['body'] = "\n".join(body)

    images = post.xpath(
        "//article//img/@src"
    )
    images = list(filter(lambda src: (src.startswith('https://')), images))
    post_info['images'] = images

    return post_info


def write_to_file(data, file_name='output.txt'):
    with open(file_name, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()


def main():
    page_url = "https://tproger.ru/"
    total_info = []

    for i in range(PAGES_COUNT):
        page_info = {}

        page_info['page'] = i+1
        page_info['url'] = page_url
        page_info['posts'] = []

        req = requests.get(page_url)
        page = html.fromstring(req.content)

        post_url_list = page.xpath(
            "//article/a/@href"
        )

        for post_url in post_url_list:
            post_info = get_info_from_url(post_url)
            page_info['posts'].append(post_info)

        total_info.append(page_info)

        page_url = get_next_page(page)
        if not page_url:
            break

        write_to_file(total_info)
        
        
if __name__ == '__main__':
    main()
