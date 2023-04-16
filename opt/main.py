from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys

from zenn_scraper import ZennScraper
from notion_manager import NotionManager

if __name__ == "__main__":
    load_dotenv()

    notion_api_key = os.environ["MIDRA_LAB_NOTION_API"]
    notion_database_id = os.environ["NOTION_DATABASE_URL"]

    publication_url = "https://zenn.dev/p/midra_lab"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    zenn_scraper = ZennScraper(publication_url)
    zenn_scraper.get_articles(driver)

    if zenn_scraper.is_articles_empty():
        driver.quit()
        sys.exit()

    notion_manager = NotionManager(notion_api_key, notion_database_id)
    notion_manager.delete_all_pages()

    for article in zenn_scraper.articles:
        details = zenn_scraper.get_article_details(driver, article)
        notion_manager.add_article(article['title'], article['url'], details['tags'], article['name'], details['date'])

    driver.quit()
