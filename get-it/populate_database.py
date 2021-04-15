from database import Database, Note
from utils import load_data
import os

def populate_db(DB_NAME='notes'):
    if DB_NAME.endswith('.db'):
        DB_NAME = DB_NAME[:-3]
        
    DB_PATH = DB_NAME + '.db'
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    db = Database(DB_NAME)
    json = load_data('./data/notes.json')

    for i in json:
        annotation = Note()
        annotation.title = list(i.values())[0]
        annotation.content = list(i.values())[1]
        db.add(annotation)
        
populate_db('teste')