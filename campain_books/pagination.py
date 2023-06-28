from rest_framework import pagination

from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 25


class CollectionsPagination(pagination.PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'


    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total': self.page.paginator.count,
                'pages': self.page.paginator.num_pages,
                'page': int(self.request.GET.get('page', DEFAULT_PAGE)),  # can not set default = self.page
                'page_size': int(self.request.GET.get('page_size', self.page_size)),
            },
            'results': data
        })
