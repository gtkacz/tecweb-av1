from django.shortcuts import render, redirect
from .models import Note

def index(request):
    if request.method=='POST':
        title=request.POST.get('titulo')
        content=request.POST.get('detalhes')
        
        note = Note(title=title, content=content)
        note.save()
                    
        return redirect('index')
    else:
        note=Note.objects.last()
        return render(request, 'notes/index.html', {'note': note})