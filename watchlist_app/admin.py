from django.contrib import admin

from watchlist_app.models import Review, StreamPlatform, Watchlist

# Register your models here.
admin.site.register(Watchlist)
admin.site.register(StreamPlatform)
admin.site.register(Review)
