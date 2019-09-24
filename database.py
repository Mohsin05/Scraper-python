from db_connection_config import db_connection

class database():

    def __init__(self):

         self.connection = db_connection.connection(self)
         mySql_Create_Table_Query = """CREATE TABLE IF NOT EXISTS jobs (Id int(11) NOT NULL AUTO_INCREMENT,
                                                               Job_id int(11) NOT NULL,
                                                               field_name text NOT NULL,
                                                               text text NOT NULL,
                                                               job_posting text NOT NULL,
                                                               created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                                               PRIMARY KEY (Id))"""
         self.cursor = self.connection.cursor()
         self.cursor.execute(mySql_Create_Table_Query)

    def isDuplicate(self, job_posting):

        #in order to abandon a resultset mid-stream.
        self.cursor = self.connection.cursor(buffered=True,dictionary=True)
        select_sql = """ SELECT Job_id FROM jobs WHERE job_posting= %s """
        insert_tuple_1 = (job_posting,)
        self.cursor.execute(select_sql, insert_tuple_1)
        result = self.cursor.fetchone()

        if result:
            return True

    def insert(self, job_id, name, value, job_posting):

        sql_insert_query = """ INSERT INTO jobs (job_id, field_name, text, job_posting) VALUES (%s,%s,%s,%s)"""
        insert_tuple_1 = (job_id+1, name, value,job_posting)
        self.cursor.execute(sql_insert_query, insert_tuple_1)
        self.connection.commit()

    def getJobId(self):

        select_sql = ('SELECT MAX(job_id) FROM jobs')
        self.cursor.execute(select_sql)
        result = self.cursor.fetchone()
        job_id = result[0] if result[0] else 0

        return job_id

