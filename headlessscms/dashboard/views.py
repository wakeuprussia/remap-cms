from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from urllib.request import Request, urlopen
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pyuploadcare import Uploadcare
uploadcare = Uploadcare(public_key='', secret_key='')

from . import serializers
from . import models

from rest_framework.decorators import api_view
from rest_framework.response import Response

import contentful
import pprint

from datetime import datetime

# Create your views here.
@api_view(['GET'])
def range(request):
    #range?start=27-02-22&end=05-03-22
    start_dt = datetime.strptime(request.query_params.get('start'), '%d-%m-%y-%H-%M')
    end_dt = datetime.strptime(request.query_params.get('end'), '%d-%m-%y-%H-%M')
    posts = models.Post.objects.order_by('-datetime').filter(datetime__gte = start_dt, datetime__lte = end_dt)
    serializer = serializers.PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def single(request, slug):
    #slug?slug=
    try:
        post = models.Post.objects.get(slug = slug)
        serializer = serializers.PostSerializer(post)
        return Response(serializer.data)
    except Exception as e:
        return Response('No Posts')


def get_posts(request):
    client = contentful.Client('', '', api_url = 'cdn.contentful.com')
    entries = client.entries({'content_type': 'post', 'limit':'1000', 'locale': '*'})
    for en in entries:
        #pprint.pprint(en.__dict__)
        #create point
        point = models.Location.objects.create(
            location = str(en.fields()['geo'][1]) +','+ str(en.fields()['geo'][0])
        )
        #get protest_type
        protest_type = models.ProtestType.objects.get(_id = en.fields()['protest_type'].fields()['id'])

        try:
            en.fields('ru')['title']
            rutitle = en.fields('ru')['title']
        except Exception as e:
            rutitle = en.fields('en-US')['title']

        try:
            en.fields('ru')['text']
            ruold_md = en.fields('ru')['text']
        except Exception as e:
            ruold_md = en.fields('en-US')['text']

        try:
            source = en.fields()['url']
        except Exception as e:
            source = None

        try:
            widget = en.fields()['tg_widget']
        except Exception as e:
            widget = None


        f =  models.Post.objects.language('ru').create(
            title = rutitle,
            old_md = ruold_md,
            slug = en.fields()['slug'],
            protest_type = protest_type,
            location = point,
            datetime = en.fields()['datetime'],
            source = source,
            widget = widget,
        )
        f.set_current_language('en')
        f.title = en.fields('en-US')['title']
        f.old_md = en.fields('en-US')['text']
        f.save()

    return HttpResponse('lol')



def get_protest_types(request):
    client = contentful.Client('', '', api_url = 'cdn.contentful.com')
    entries = client.entries({'content_type': 'type', 'limit':'1000', 'locale': '*'})
    for en in entries:
        # pprint.pprint(en.__dict__)
        print(en.fields()['id'])
        print(en.fields()['title'])
        print(en.fields('ru')['title'])

        f =  models.ProtestType.objects.language('ru').create(
            name=en.fields('ru')['title'],
            _id=int(en.fields()['id'])
        )

        f.set_current_language('en')
        f.name = en.fields()['title']

        f.save()

    return HttpResponse('lol')



class ImageUploadView(View):
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return JsonResponse(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            try:
                image = uploadcare.upload(the_file, size=the_file.size, store=True)
                print(image.cdn_url)
                return JsonResponse({'success': 1, 'file': {"url": image.cdn_url}})
            except Exception as e:
                print(e)
                return JsonResponse({'success': 0})
