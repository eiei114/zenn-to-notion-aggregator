from notion_client import Client


class NotionManager:
    def __init__(self, api_key, database_id):
        self.notion = Client(auth=api_key)
        self.database_id = database_id

    def add_article(self, title, url, tags, name, date):
        new_page = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Tags": {"multi_select": [{"name": tag} for tag in tags]},
            "Link": {"url": url},
            "Author": {"rich_text": [{"text": {"content": name}}]},
            "Date": {"date": {"start": date}}
        }
        self.notion.pages.create(parent={"database_id": self.database_id}, properties=new_page)

    def delete_all_pages(self):
        pages = self.notion.databases.query(database_id=self.database_id)
        for page in pages['results']:
            self.notion.pages.update(page_id=page['id'], archived=True)
