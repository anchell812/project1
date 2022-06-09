from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news_mail']


url = 'https://news.mail.ru'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61/63 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

news = dom.xpath("//a[@class='list__text']")
for news in news:
    list = {}
    list['type'] = 'Mail.ru_news'
    list['content'] = news.xpath('.//text()')[0].replace('\xa0', ' ')
    list['news_link'] = news.xpath('.//@href')[0]
    response_news = requests.get(list['news_link'], headers=headers)
    dom_news = html.fromstring(response_news.text)
    list['news_date'] = dom_news.xpath("//span[contains(@class, 'note__text')]//@datetime")[0]
    db.news_mail.update_one({'news_link': list['news_link']}, {'$set': list}, upsert=True)

for el in db.news_mail.find({}):
    print(el)