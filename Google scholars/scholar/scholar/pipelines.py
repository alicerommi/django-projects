# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from .database import create_table,db


class ScholarPipeline:
    def __init__(self):
        self.cursor = None
        self.query = None
        self.run_db()
        self.table.create_tablescholar()

    def run_db(self):
        self.db = db()
        self.conn = self.db.conn
        self.cursor = self.conn.cursor()
        self.table = create_table(self.conn)

    def process_item(self, item, spider):
        if spider.name == "titlecrawler":
            self.store_titles(item)
        return item

    def store_titles(self, item):

        self.query = """insert into gscholar (title) values (%s)"""
        self.cursor.execute(self.query, (
            item['title'],
        ))
        self.conn.commit()
