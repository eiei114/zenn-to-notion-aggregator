from bs4 import BeautifulSoup
from datetime import datetime


class ZennScraper:
    def __init__(self, url):
        self.url = url
        self.articles = []

    def get_articles(self, driver):
        driver.get(self.url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article', class_='ArticleCard_container__3qUYt')

        for article in articles:
            title = article.find('h3', class_='ArticleCard_title__UnBHE').text
            url = "https://zenn.dev" + article.find('a', class_='ArticleCard_mainLink__X2TOE')['href']
            name = article.find('div', class_='ArticleCard_userName__1q_wZ').text
            self.articles.append({'title': title, 'url': url, 'name': name})

    def is_articles_empty(self):
        return len(self.articles) == 0

    def get_article_details(self, driver, article):
        driver.get(article['url'])

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        date = soup.find('span', class_='ArticleHeader_num__rSDj6').text
        date_obj = datetime.strptime(date, '%Y/%m/%d')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        tags_container = soup.find('div', class_='View_topics__OVMdM')
        tags = tags_container.find_all('div', class_='View_topicName__rxKth')

        results = []
        for tag in tags:
            results.append(tag.text)

        return {"tags": results, "date": formatted_date}
