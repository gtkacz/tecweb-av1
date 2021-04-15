import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self, DB_NAME):
        self.DB_NAME = self.__DB_PATH__(DB_NAME)
        self.conn = sqlite3.connect(self.DB_NAME)
        self.TABLE_NAME = "note"
        self.CREATE_ACTION = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL);'
        self.conn.execute(self.CREATE_ACTION)
        self.conn.commit()
        
    def add(self, note):
        self.ADD_ACTION = f'INSERT INTO {self.TABLE_NAME} (title, content) VALUES ("{note.title}", "{note.content}");'
        self.conn.execute(self.ADD_ACTION)
        self.conn.commit()
        
    def get_all(self):
        self.select = "SELECT id, title, content FROM note"
        self.cursor = self.conn.execute(self.select)
        self.READ_NOTE = []
        for row in self.cursor:
            self.READ_NOTE.append(Note(row[0], row[1], row[2]))
        return self.READ_NOTE
    
    def update(self, entry):
        if (entry.id is not None) and (entry.content is not None) and (entry.title is not None):
            self.UPDATE_ACTION = f"UPDATE {self.TABLE_NAME} SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}"
            self.conn.execute(self.UPDATE_ACTION)
            self.conn.commit()
        else:
            raise TypeError("Function can't receive NoneType as argument.")
        
    def delete(self, note_id):
        self.DELETE_ACTION = f"DELETE FROM {self.TABLE_NAME} WHERE id = {note_id};"
        self.conn.execute(self.DELETE_ACTION)
        self.conn.commit()
        
    def __DB_PATH__(self, DB_NAME):
        try:
            DB_NAME = str(DB_NAME)
            if not DB_NAME.endswith('.db'):
                return (DB_NAME + '.db')
            else:
                return (DB_NAME)
        except:
            raise ValueError("Did not enter a valid file name.")