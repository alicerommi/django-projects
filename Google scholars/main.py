import os
from scholar.scholar.database import create_table,db
class run:
    def __init__(self):
        self.db = db()
        self.conn = self.db.conn
        self.cTable = create_table(self.conn)
        self.owd = os.getcwd()
        os.system('ls')
        os.chdir('scholar')
    def scraptitles(self,keyword):
            self.cTable.delete_table_scholar()
            self.cTable.create_tablescholar()
            query = 'scrapy crawl titlecrawler -a query="' + keyword + '"'
            try:
                os.system(query)
            finally:
                os.chdir(self.owd)
                self.owd = os.getcwd()


