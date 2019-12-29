# -*- coding: utf-8 -*-
# !/usr/bin/env python
import requests
from datetime import datetime
from lxml import html
import traceback
import time
import csv

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                         data['date'],
                         data['blockqoute'],
                         data['text'],) )

        print(data['title'], 'text')
try:
    while True:
        time.sleep(30)
        url = 'https://www.zakon.kz/news/page/0/'
        url2 = 'https://www.zakon.kz/'
        parsed_body = html.fromstring(requests.get(url).text)
        a = parsed_body.xpath('//a[@class="tahoma font12"]/@href')
        links = []
        for link in a:
            links.append(url2 + link)
            print(links)
        for new_link in links:
            parsed_body_change = html.fromstring(requests.get(new_link).text)
            times = [item.lstrip("$") for item in parsed_body_change.xpath('//span[@class="news_date"]//span/text()')]
            if datetime.fromtimestamp(time.time() - 240).strftime("%H:%M") in times:
                text = [item.lstrip("$") for item in parsed_body_change.xpath('//span[@class="news_date"]/text()')]
                title = [item.lstrip("$") for item in parsed_body_change.xpath('//h1/text()')]
                info = [item.lstrip("$") for item in parsed_body_change.xpath('//p/text()')]
                blockqoute = [item.lstrip("$") for item in parsed_body_change.xpath('//blockquote[@class="quote_in_news"]/text()')]
                data = {'title': [],
                        'text': [],
                        'date': [],
                        'blockqoute': [],}
                for a, b in enumerate(text):
                    data['title'] += title
                    data['date'] += text
                    data['text'] += info
                    data['blockqoute'] += blockqoute
                    write_csv(data)
except Exception as e:
    print('Ошибка:\n', traceback.format_exc())


