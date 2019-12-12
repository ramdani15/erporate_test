from rest_framework import pagination, response


class ResultPagination(pagination.PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'results': data
        })
