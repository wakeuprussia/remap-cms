from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('editorjs/image_upload/', staff_member_required(views.ImageUploadView.as_view()), name='custom_upload'),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('martor/', include('martor.urls')),

    path('get_protest_types', views.get_protest_types, name = 'get_protest_types'),
    path('get_posts', views.get_posts, name = 'get_posts'),

    #api
    path('range', views.range, name='range'),#range?start=27-02-22&end=05-03-22
    path('single/<slug:slug>', views.single, name='single')
]
