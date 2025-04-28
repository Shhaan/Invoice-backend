from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

def get_response(error,data,status):
    return Response({"error":error,"message":data},status=status)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'   
    max_page_size = 100