
from django.urls import path, include
import django_filters
from watchlist_app.api.views import EmailReviewList, ReviewDetail, ReviewCreate, ReviewList, ReviewsVS,  StreamPlatformVS, UserReviewList, WatchlistAA, WatchlistVS, update_agora_token
from rest_framework.routers import DefaultRouter
from watchlist_app.models import Watchlist
stream_router = DefaultRouter()
stream_router.register("stream", StreamPlatformVS, basename="stream-platform")
stream_router.register("movies", WatchlistVS, basename="movies")
stream_router.register("reviews-all", ReviewsVS, basename="reviews-all")
urlpatterns = [


    path('', include(stream_router.urls)),
    path("movies/<int:pk>/reviews/", ReviewList().as_view(), name="reviews-movie"),
    path("reviews/<int:pk>", ReviewDetail().as_view(), name="review-detail"),
    path("movies/<int:pk>/review-create/",
         ReviewCreate().as_view(), name="review-create"),
    path("reviews-user/<str:username>/",
         UserReviewList().as_view(), name="user-view-list"),
    path("reviews-email/",
         EmailReviewList().as_view(), name="email-view-list"),
    path("movie-list/",
         WatchlistAA().as_view(), name="movie-list"),
     path("token/" , update_agora_token , name="update-token")
]
