from wsgiref.validate import validator
from rest_framework import serializers as s

from watchlist_app.models import Review, StreamPlatform, Watchlist


class ReviewSerializer(s.ModelSerializer):
    review_user = s.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class WatchlistSerializer(s.ModelSerializer):
    platform = s.SlugRelatedField(
        "name", queryset=StreamPlatform.objects.all())

    class Meta:
        model = Watchlist
        fields = "__all__"
        read_only_fields = ['avg_rating', 'rating_num']


class StreamPlatformSerializer(s.ModelSerializer):
    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
