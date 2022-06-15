from django.db import models
from django.utils.text import slugify
from django_editorjs_fields import EditorJsJSONField
from parler.models import TranslatableModel, TranslatedFields
from mapbox_location_field.models import LocationField
from django.utils import timezone

class ProtestCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
    )
    _id = models.IntegerField(null=True)

    def __str__(self):
         return self.name

class ProtestType(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
    )
    _id = models.IntegerField(null=True)

    def __str__(self):
         return self.name

class Location(models.Model):
    location = LocationField(null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            locat = self.location.split(',')
            self.lat = locat[1]
            self.lon = locat[0]
        except Exception as e:
            self.lat = self.location[1]
            self.lon = self.location[0]
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
         return str(self.location)

# Create your models here.
class Post(TranslatableModel):
    id = models.BigAutoField(primary_key=True)
    translations = TranslatedFields(
        title = models.CharField(max_length=255),
        body_editorjs = EditorJsJSONField(default=None, null=True),
        old_md = models.TextField(null=True, blank=True)
    )
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    protest_type = models.ForeignKey(
        'ProtestType',
        on_delete=models.CASCADE,
        null=True
    )
    protest_category = models.ForeignKey(
        'ProtestCategory',
        on_delete=models.CASCADE,
        null=True
    )
    location = models.OneToOneField(
        'Location',
        on_delete=models.CASCADE,
        null=True
    )
    source = models.URLField(null=True, blank=True)
    widget = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    #city

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def is_published(self):
        return self.published == True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
