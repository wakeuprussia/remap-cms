from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Post, ProtestCategory, ProtestType, Location
from mapbox_location_field.admin import MapAdmin

admin.site.site_header = "reMap - Администрирование"

@admin.action(description='Опубликовать выбранное')
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)

@admin.action(description='Снять выбранное с публикации')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)


class PostAdmin(TranslatableAdmin):
    actions = [make_published, make_unpublished]
    list_display = ('title','slug','protest_type', 'protest_category', 'published', 'datetime', 'created_date')
    list_editable = ('published',)
    search_fields = ('translations__title',)
    readonly_fields = ('id',)
    fieldsets = (
        ("C переводом", {
            'fields': ('title','body_editorjs','old_md'),
        }),
        ("Без перевода", {
            'fields': ('id','slug','protest_type','protest_category', 'location', 'source', 'widget', 'published', 'datetime')
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',)
        }



class ProtestCategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        ("C переводом", {
            'fields': ('name',),
        }),
        ("Без перевода", {
            'fields': ('_id',)
        }),
    )

class ProtestTypeAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        ("C переводом", {
            'fields': ('name',),
        }),
        ("Без перевода", {
            'fields': ('_id',)
        }),
    )

admin.site.register(Post, PostAdmin)
admin.site.register(ProtestCategory, ProtestCategoryAdmin)
admin.site.register(ProtestType, ProtestTypeAdmin)
admin.site.register(Location, MapAdmin)
