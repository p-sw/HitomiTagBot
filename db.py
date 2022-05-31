from settings import base
import psycopg2

class Databases:
    def __init__(self, db_obj):
        self.db = psycopg2.connect(host=db_obj['DATABASE_HOST'], 
                                   dbname=db_obj['DATABASE'],
                                   user=db_obj['DATABASE_USER'],
                                   password=db_obj['DATABASE_PASSWORD'],
                                   port=5432)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
    
    def execute_result(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

DB_OBJECT = Databases(base.DATABASE)

DB_OBJECT.execute('CREATE TABLE IF NOT EXISTS Tags(prefix varchar(64), tag varchar(64), tag_num int)')
DB_OBJECT.commit()