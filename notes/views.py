from django.shortcuts import render, redirect
from .models import Note, Tag


def parse_tags(tags_text):
    nomes = [nome.strip() for nome in tags_text.split(',') if nome.strip()]
    tags = []
    for nome in nomes:
        tag, created = Tag.objects.get_or_create(name=nome)
        tags.append(tag)
    return tags


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tags_text = request.POST.get('tag', '')

        note = Note.objects.create(title=title, content=content)
        note.tags.set(parse_tags(tags_text))

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
        tags_text = request.POST.get('tag', '')

        note.save()
        note.tags.set(parse_tags(tags_text))

        return redirect('index')
    else:
        return render(request, 'notes/update.html', {'note': note})


def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    notes = tag.note_set.all()
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})