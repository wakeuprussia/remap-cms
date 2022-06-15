from rest_framework import serializers
from . import models

class ProtestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProtestType
        fields = ['name', '_id']

class ProtestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProtestCategory
        fields = ['name', '_id']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ['location', 'lat', 'lon']

class PostSerializer(serializers.ModelSerializer):
    protest_type = ProtestTypeSerializer(read_only=True)
    protest_category = ProtestCategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = ['id' ,'title','slug','location', 'old_md','body_editorjs','protest_type', 'protest_category', 'source', 'widget', 'datetime']
