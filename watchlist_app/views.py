# from django.http import JsonResponse
# from django.shortcuts import render
# from watchlist_app.models import Movie
# from rest_framework.decorators import api_view
# # Create your views here.


# @api_view(['GET'])
# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         "movies": list(movies.values())
#     }
#     return JsonResponse(data)


# def movie_detail(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         "movie": movie
#     }
#     return JsonResponse(data)
