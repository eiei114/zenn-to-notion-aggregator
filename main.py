from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notion_client import Client
from dotenv import load_dotenv
import os

def get_zenn_articles(publication_url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(publication_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    articles = soup.find_all('article', class_='ArticleCard_container__3qUYt')

    results = []
    for article in articles:
        title = article.find('h3', class_='ArticleCard_title__UnBHE').text
        url = "https://zenn.dev" + article.find('a', class_='ArticleCard_mainLink__X2TOE')['href']
        name = article.find('div', class_='ArticleCard_userName__1q_wZ').text
        results.append({'title': title, 'url': url, 'name': name})
        print(f"{title} - {url} - {name}")
        print("取得できた？")
    return results

publication_url = "https://zenn.dev/p/midra_lab"

# 環境変数を読み込み
load_dotenv()

# Notion APIキーを環境変数から取得
notion_api_key = os.environ["MIDRA_LAB_NOTION_API"]

# NotionデータベースIDを設定
notion_database_id = os.environ["NOTION_DATABASE_URL"]

# Notionクライアントを初期化
notion = Client(auth=notion_api_key)

def add_article_to_notion_database(title, url, author):
    new_page = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Author": {"rich_text": [{"text": {"content": author}}]},
        "Link": {"url": url}
    }
    notion.pages.create(parent={"database_id": notion_database_id}, properties=new_page)

articles = get_zenn_articles(publication_url)

for article in articles:
    add_article_to_notion_database(article['title'], article['url'], article['name'])
