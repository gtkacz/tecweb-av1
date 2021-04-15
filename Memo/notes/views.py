from django.shortcuts import render, redirect
from .models import Note

def index(request):
    if request.method=='POST':
        content=request.POST.get('content')
        
        note = Note(content=content)
        note.save()
                    
        return redirect('index')
    else:
        note=Note.objects.last()
        return render(request, 'notes/index.html', {'note': note})