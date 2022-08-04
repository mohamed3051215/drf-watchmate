from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from watchlist_app.api.paginition import MoviesPaginition, ReviewCPagination, ReviewsLOPaginition
from watchlist_app.api.permissions import ReviewUserOrReadOnly, isAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchlistSerializer
from rest_framework.response import Response
from watchlist_app.api.throttling import ReviewDetailsThrottle, ReviewListThrottle
from watchlist_app.models import Review, StreamPlatform, Watchlist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie: Watchlist = Watchlist.objects.get(pk=pk)

        review_user = self.request.user
        review_query = Review.objects.filter(
            watchlist=movie, review_user=review_user)
        if review_query.exists():
            raise ValidationError(
                "This use has reviewed this movie already, can't make more than on review")

        movie.rating_num += 1
        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data["rating"]
        else:
            movie.avg_rating = (
                movie.avg_rating * (movie.rating_num - 1) + serializer.validated_data["rating"]) / movie.rating_num
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        reviews = Review.objects.filter(watchlist=pk)
        return reviews


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # throttle_classes = [ReviewDetailsThrottle]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminUser]


class WatchlistVS(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [isAdminOrReadOnly]
    # pagination_class = MoviesPaginition


class WatchlistAA(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating', 'rating_num']


class UserReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


class EmailReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        email = self.request.query_params.get("email", None)
        query_set = Review.objects.all()
        if email is not None:
            return query_set.filter(review_user__email=email)

        return query_set


class ReviewsVS(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = ReviewCPagination
