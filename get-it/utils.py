from pathlib import Path
import json, os
from database import Database, Note
from localStoragePy import localStoragePy
from urllib.parse import unquote_plus

def extract_route(request):
    if request.startswith('POST'):
        request=restore_db(request, 'teste')
    if request != '':
        return request.split()[1][1:]
    else:
        return ''

def is_path(subject):
    if not type(subject) is Path:
        return Path(subject)
    else:
        return subject
        
def read_file(path):
    path = is_path(path)
    extension = path.suffix
    target = ['.txt', '.html', '.css', '.js']
    if extension in target:
        with open(path, 'rt', encoding = 'utf-8') as file:
            data = file.read()
        return data.encode(encoding = 'UTF-8')
    else:
        with open(path, 'rb') as file:
            data = file.read()
        return data
    
def has_directory(string, directory):
    c = 0
    string = str(string)
    for i in string:
        if i == '/':
            c += 1
    if c > 1:
        return str(string)
    else:
        return str(f'./{directory}/{string}')

def load_data(path):
    path = has_directory(path, 'data')
    with open(path, encoding = 'utf-8') as file: 
        data = json.load(file)
    return data

def load_template(name):
    path = has_directory(name, 'templates')
    return (read_file(path)).decode(encoding = 'UTF-8')

def build_response(body = '', code = 200, reason = 'OK', headers = ''):
    args = [str(code), reason]
    response = 'HTTP/1.1 ' + (' '.join(args))
    if headers == '':
        response += '\n\n' + body
    else:
        response += '\n' + headers + '\n\n' + body
    return response.encode(encoding = 'UTF-8')

def write_json(data, filename):
    path = has_directory(filename, 'data')
    with open(path, 'r', encoding = 'utf-8') as file:
        write = json.load(file)
        write.append(data)
    
    with open(path, 'w', encoding = 'utf-8') as file:
        json.dump(write, file, ensure_ascii = False, indent = 4)
        
def key_is_empty(dic, key):
    a=dic.get(key)
    if a is not None:
        return a
    else:
        raise ValueError(f"Dictionary has no key {key}")
        
def write_on_db(data, DB_NAME):
    if DB_NAME.endswith('.db'):
        db = DB_NAME[-3]
    else:
        db = DB_NAME
        
    db=Database(db)
        
    if type(data) == Note:
        db.add(data)
        
    elif type(data) == dict:
        try:
            annotation = Note()
            annotation.title = str(key_is_empty(data,'titulo'))
            annotation.content = str(key_is_empty(data,'detalhes'))
            db.add(annotation)
        except:
             for key, value in data.items():
                 annotation = Note()
                 annotation.title = str(key)
                 annotation.content = str(value)
                 db.add(annotation)
            
    elif type(data) == list:
            for i in data:
                annotation = Note()
                annotation.title = list(i.values())[0]
                annotation.content = list(i.values())[1]
                db.add(annotation)
                
    else:
        raise TypeError("Provided data could not be appended to database.")
    
def delete_from_db(id, db_name):
    pass

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

def restore_db(request, db_name='notes'):
    request2 = request.replace('\r', '')
    true=request2.split('\n')
    true=(true[-1]).split('&')
    if true[-1]=='restore-db=restore-db':
        populate_db(db_name)
        return ''
    else:
        return request
    
def process_post(request, db=Database('notes')):
    is_restore=False
    is_delete=False
    is_edit=False
    
    if (request.split()[-1]).split('&')[-1]=='restore-db=restore-db':
        is_restore=True
            
    if ((request.split()[-1]).split('&')[-1]).split('=')[0]=='delete_note_id':
        note_id=((request.split()[-1]).split('&')[-1]).split('=')[1]
        db.delete(note_id)
        is_delete=True
        
    if ((request.split()[-1]).split('=')[0])=='edit_note_id':
        note_id=(((request.split()[-1]).split('=')[1]).split('&')[0])
        note_title=unquote_plus(((request.split()[-1]).split('&')[1]).split('=')[1])
        note_content=unquote_plus(((request.split()[-1]).split('&')[2]).split('=')[1])
        
    #     note_id=((request.split()[-1]).split('&')[-1]).split('=')[1]
    #     note_title=unquote_plus((request.split()[-1]).split('&')[0]).split('=')[1]
    #     note_content=unquote_plus((request.split()[-1]).split('&')[1]).split('=')[1]
        try:
            edit=Note()
            edit.id=note_id
            edit.title=note_title
            edit.content=note_content
            db.update(edit)
        except:
            pass
        
        if note_id != None:
            is_edit=True
        
    return is_restore, is_delete, is_edit