from concurrent.futures import ThreadPoolExecutor

from notion_client import Client


class NotionManager:
    def __init__(self, api_key, database_id):
        self.notion = Client(auth=api_key)
        self.database_id = database_id

    def add_article(self, title, url, tags, date):
        new_page = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Tags": {"multi_select": self.get_tags_and_remove_default_tag(tags)},
            "Link": {"url": url},
            "Date": {"date": {"start": date}}
        }
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=new_page)

    # Get the list of tags with zenn's default tag removed from tags
    def get_tags_and_remove_default_tag(self, tags) -> list:
        notion_tags = []
        for tag in tags:
            if tag not in ["tech", "idea"]:
                notion_tags.append({"name": tag})
        return notion_tags

    def delete_page(self,page_id):
        self.notion.pages.update(page_id=page_id, archived=True)

    def delete_all_pages(self):
        pages = self.notion.databases.query(database_id=self.database_id)
        with ThreadPoolExecutor() as executor:
            # ページを並列で削除する
            [executor.submit(self.delete_page, page['id']) for page in pages['results']]
