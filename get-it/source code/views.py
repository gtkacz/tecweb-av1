from urllib.parse import unquote_plus
#from utils import *
from utils import load_template, build_response, process_post, write_on_db
from database import Database, Note

def request_params(request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    for valor in corpo.split('&'):
        key = unquote_plus(valor.split('=')[0])
        value = unquote_plus(valor.split('=')[1])
        params[key] = value
    return params

def index(request):
    note_template = load_template('components/note.html')
    dados=Database('teste')
    db_notes=dados.get_all()
    
    if request.startswith('GET'):
        # Cria uma lista de < li > 's para cada anotação
        # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        notes_li = [
            note_template.format(title = dados.title, details = dados.content, id=dados.id)
            for dados in db_notes
        ]
        notes = '\n'.join(notes_li)
        return build_response() + load_template('index.html').format(notes = notes).encode(encoding = 'utf-8')
    
    elif request.startswith('POST'):
        params = request_params(request)
        
        is_restore, is_delete, is_edit = process_post(request, Database('teste'))
        
        if (is_restore == False) and (is_delete == False) and (is_edit == False):
            write_on_db(params, 'teste')
            
        return build_response(code = 303, reason = 'See Other', headers = 'Location: /')
    
def not_found():
    return build_response(body = '404\nPage Not Found', code = 404, reason = 'Not Found') + load_template('404.html').encode(encoding='utf-8')