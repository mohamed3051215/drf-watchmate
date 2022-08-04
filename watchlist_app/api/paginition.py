from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class MoviesPaginition(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class ReviewsLOPaginition(LimitOffsetPagination):
    default_limit = 5
    offset_query_param = 'start'
    max_limit = 10


class ReviewCPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10
    cursor_query_param = 'start'
    ordering = 'created'

    def get_paginated_response(self, data):
        return Response({"links": {
            "next": self.get_next_link(),
            "previous": self.get_previous_link()
        }, "count": self.page.paginator.count, "item_count_recieved": self.page_size, "data": data})
