from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .models import Beer, Tag
from .serializers import BeerSerializer


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = None

        # verifica se o cabra preencheu o mínimo necessário mesmo
        if ((title.replace(" ", "") == "") or (content.replace(" ", "") == "")):
            return render(
                request=request, 
                template_name='beers/index.html', 
                context={ 
                    'beers': Beer.objects.all(),
                    "msg_error": "O título e o conteúdo não podem estar vazios!"
                }
            )

        all_tags = Tag.objects.all()

        # Verifica se uma tag foi inserida
        if request.POST.__contains__('tag'):
            tag_input = request.POST.get('tag')
            # verifica se a tag não está vazia
            if tag_input.replace(" ", "") != "":
                tag = Tag(text=tag_input)
                # verifica se a tag já existe
                for tag_db in all_tags:
                    if tag_db.text == tag_input:
                        tag = tag_db
                        break

        new_beer = Beer(title=title, content=content, tag=tag)

        # request para criar nota
        if request.POST.__contains__('create'):
            if tag is not None:
                tag.save()
            new_beer.save()
        
        # Verifica se contém id (para solicitações de delete)
        if request.POST.__contains__('id'):
            beer_id = request.POST.get('id')
            beer = Beer(id=beer_id, content=content, tag=tag)

        # request para deletar beer
        if request.POST.__contains__('delete'):
            beer.delete()

        return redirect('/')
    else:
        all_beers = Beer.objects.all()
        return render(
            request=request, 
            template_name='beers/index.html', 
            context={ 'beers': all_beers }
        )


def tags(request):
    all_tags = Tag.objects.all()
    count = {}
    for tag in all_tags:
        count[tag.id] = Beer.objects.filter(tag__id__exact=tag.id).count() or 0

    context = { 
        "tags": all_tags, 
        "counter": count
    }
    
    return render(
        request=request,
        template_name='beers/tags.html',
        context=context
    )



def beer_view(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    tag_entry = beer.tag

    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = tag_entry

        # verifica se o cabra preencheu o mínimo necessário mesmo
        if ((title.replace(" ", "") == "") or (content.replace(" ", "") == "")):
            return render(
                request=request, 
                template_name='beers/beer_view.html', 
                context={ 
                    'beer': beer,
                    "msg_error": "O título e o conteúdo não podem estar vazios!"
                }
            )

        all_tags = Tag.objects.all()

        # Verifica se uma tag foi inserida
        if request.POST.__contains__('tag'):
            tag_input = request.POST.get('tag')
            # verifica se a tag não está vazia
            if tag_input.replace(" ", "") != "":
                tag = Tag(text=tag_input)
                # verifica se a tag já existe
                for tag_db in all_tags:
                    if tag_db.text == tag_input:
                        tag = tag_db
                        break

        beer_updated = Beer(id=beer_id, title=title, content=content, tag=tag)

        # request para atualizar nota
        if request.POST.__contains__('update'):
            if ((tag is not None) and (tag not in all_tags)):
                tag.save()
            beer.delete()
            beer_updated.save()

        return redirect('/')

    else:
        return render(
            request=request,
            template_name='beers/beer_view.html',
            context={ "beer": beer }
        )


def beers_by_tag(request, tag_id):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = get_object_or_404(Tag, pk=tag_id)

        all_tags = Tag.objects.filter(id__exact=tag_id)

        # Verifica se uma tag foi inserida
        if request.POST.__contains__('tag'):
            tag_input = request.POST.get('tag')
            # verifica se a tag não está vazia
            if tag_input.replace(" ", "") != "":
                tag = Tag(text=tag_input)
                # verifica se a tag já existe
                for tag_db in all_tags:
                    if tag_db.text == tag_input:
                        tag = tag_db
                        break

        new_beer = Beer(title=title, content=content, tag=tag)

        # request para criar nota
        if request.POST.__contains__('create'):
            if tag is not None:
                tag.save()
            new_beer.save()
        
        # Verifica se contém id (para solicitações de delete)
        if request.POST.__contains__('id'):
            beer_id = request.POST.get('id')
            beer = Beer(id=beer_id, content=content, tag=tag)

        # request para deletar beer
        if request.POST.__contains__('delete'):
            beer.delete()

        return redirect('/')
    else:
        all_beers = Beer.objects.all().filter(tag__id__exact=tag_id)
        tag_ = get_object_or_404(Tag, pk=tag_id)
        return render(
            request=request, 
            template_name='beers/beers_by_tag.html', 
            context={
                'beers': all_beers,
                'tag': tag_
            }
        )

@api_view(['GET', 'POST'])
def api_beer(request, beer_id):
    try:
        beer = Beer.objects.get(id=beer_id)
    except Beer.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        new_beer_data = request.data
        beer.title = new_beer_data['title']
        beer.content = new_beer_data['content']
        beer.save()
    
    serialized_beer = BeerSerializer(beer)
    return Response(serialized_beer.data)