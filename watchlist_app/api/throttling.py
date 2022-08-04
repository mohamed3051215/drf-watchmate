from rest_framework.throttling import UserRateThrottle
import django_filters


class ReviewDetailsThrottle(UserRateThrottle):
    scope = "review-detail"


class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"
