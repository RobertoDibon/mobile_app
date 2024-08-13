import sqlite3

def create_table():
    conn = sqlite3.connect('src\db\data_user.db')
    cursor = conn.cursor()
    
    #Verifying if the table already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data_user';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        query = '''CREATE TABLE data_user (
                    id INTEGER PRIMARY KEY,
                    REFERENCE VARCHAR(15),
                    USER VARCHAR(20),
                    PASSWORD VARCHAR(10)
                    ); 
                '''
        cursor.execute(query)
        conn.commit()

    # else:
    #     print("There is a database already, connecting...")

    conn.close()


class DbDataUser:
    create_table()
    def __init__(self) -> None:
        self.conn = sqlite3.connect(r"src\db\data_user.db", check_same_thread = False)


    def add_reference(self, reference, user, password):
        query = '''INSERT INTO data_user (REFERENCE, USER, PASSWORD)
                    VALUES (?,?,?)
                '''
        self.conn.execute(query, (reference, user, password))
        self.conn.commit()

    def get_reference(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM data_user"
        cursor.execute(query)
        references = cursor.fetchall()
        return references
    
    def delete_reference(self, reference):
        query = "DELETE FROM data_user WHERE ID =?"
        self.conn.execute(query, (reference,))
        self.conn.commit()

    def update_reference(self, data_id, reference, user, password):
        query = '''UPDATE data_user SET REFERENCE =?, USER =?, PASSWORD =? WHERE ID =?'''
        self.conn.execute(query, (reference, user, password, data_id))
        self.conn.commit()

    def close_conn(self):
        self.conn.close()
        
class DbUser:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(r"src\db\user.db", check_same_thread = False)

    def add_password(self, password):
        query = '''INSERT INTO user (PASSWORD)
                    VALUES (?)
                '''
        self.conn.execute(query, (password,))
        self.conn.commit()

    def has_records(self):
        cursor = self.conn.cursor()
        query = "SELECT COUNT(*) FROM user"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] > 0 
    
    def get_password(self):
        cursor = self.conn.cursor()
        query = "SELECT password FROM user"
        cursor.execute(query)
        result = cursor.fetchone()
        return result [0]

   
    


