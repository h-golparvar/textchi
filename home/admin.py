from django.contrib import admin

from . import models



class SingerAdmin(admin.ModelAdmin):
    fields = ['fa_name', 'en_name', 'description', 'picture', 'slug']


admin.site.register(models.Singer)


class GenreAdmin(admin.ModelAdmin):
    fields = ['name', 'picture', 'description', 'meta_title', 'meta_description', 'sub_genre', 'is_sub', 'slug']


admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Song)
admin.site.register(models.Comment)
admin.site.register(models.Album)
