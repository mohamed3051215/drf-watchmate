import time
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from watchlist_app import models
from watchlist_app.api import serializers as s


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="mohamed", password="mohamedayman")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix", about="shit", website="https://netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "The most discusting",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse("stream-platform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("stream-platform-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_ind(self):
        response = self.client.get(
            reverse("stream-platform-detail", args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete(self):
        response = self.client.delete(
            reverse("stream-platform-detail", args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_put(self):
        data = {
            "name": "Mappa",
            "about": "The best",
            "website": "https://mappa.com/"
        }
        response = self.client.put(
            reverse("stream-platform-detail", args=(self.streamplatform.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="mohamed", password="mohamedayman")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix", about="shit", website="https://netflix.com")
        self.movie = models.Watchlist.objects.create(
            platform=self.streamplatform, title="Example", storyline="storyline", active=True)

    def test_movies_create(self):
        data = {
            "platform": self.streamplatform,
            "title": "example",
            "storyline": "storylin",
            "active": True,
        }
        response = self.client.post(reverse("movies-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movies_list(self):
        response = self.client.get(reverse("movies-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movies_retrieve(self):
        response = self.client.get(
            reverse("movies-detail", args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movies_delete(self):
        response = self.client.delete(
            reverse("movies-detail", args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movies_put(self):
        data = {
            "platform": self.streamplatform,
            "title": "example",
            "storyline": "storylin",
            "active": True,
        }
        response = self.client.post(
            reverse("movies-detail", args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.Watchlist.objects.count(), 1)
        self.assertEqual(models.Watchlist.objects.get().title,
                         "Example")


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="mohamed", password="mohamedayman")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix", about="shit", website="https://netflix.com")
        self.movie = models.Watchlist.objects.create(
            platform=self.streamplatform, title="Example", storyline="storyline", active=True)
        self.movie2 = models.Watchlist.objects.create(
            platform=self.streamplatform, title="example", storyline="storyline", active=True)
        self.review = models.Review.objects.create(
            rating=5, review_user=self.user, description="Review", active=True, watchlist=self.movie2)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "great",
            "watchlist": self.movie.id,
            "active": True
        }
        response = self.client.post(
            reverse("review-create", args=(self.movie.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Watchlist.objects.get(
            title="Example").avg_rating, 5)

    def test_review_create_unauthed(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "great",
            "watchlist": self.movie.id,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("review-create", args=(self.movie.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "s",
            "watchlist": self.movie.id,
            "active": False
        }
        response = self.client.put(
            reverse("review-detail", args=(self.review.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse("reviews-movie", args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(
            reverse("review-detail", args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TokenTestCase(APITestCase):

    def test_update_token(self):
        appID = "970CA35de60c44645bbae8a215061b33"
        appCertificate = "5CFd2fd1755d40ecb72977518be15d3b"
        channelName = "7d72365eb98348539asdf3f9d460bdda"

        userAccount = "2882341273"
        expireTimeInSeconds = 3600
        currentTimestamp = int(time.time())

        response = self.client.get(
            f"/watch/token/?app_id={appID}&APC={appCertificate}&channel_name={channelName}&account={userAccount}", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
