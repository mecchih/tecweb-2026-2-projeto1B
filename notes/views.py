from django.shortcuts import render, redirect
from .models import Note, Tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag_name = request.POST.get('tag', '').strip()

        tag = None
        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)

        Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})


def delete(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('index')


def update(request, note_id):
    note = Note.objects.get(id=note_id)

    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        tag_name = request.POST.get('tag', '').strip()

        if tag_name:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            note.tag = tag
        else:
            note.tag = None

        note.save()
        return redirect('index')
    else:
        return render(request, 'notes/update.html', {'note': note})


def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    notes = Note.objects.filter(tag=tag)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})