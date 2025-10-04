
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20               # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class TimestampBasedPagination(PageNumberPagination):
    """
    Custom pagination for timestamp-based pagination.
    Returns next/previous URLs with timestamp and type parameters.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        # Get the current request
        request = self.request
        
        # Get timestamp and type from request
        current_timestamp = request.query_params.get('timestamp')
        pagination_type = request.query_params.get('type', 'old')
        
        # Determine next and previous URLs
        next_url = None
        previous_url = None
        
        if self.page.has_next():
            # Get the last item's timestamp for next page
            last_item = data[-1] if data else None
            if last_item and hasattr(last_item, 'created_at'):
                next_timestamp = last_item.created_at.isoformat()
                next_url = f"{request.build_absolute_uri()}?timestamp={next_timestamp}&type=old"
        
        if self.page.has_previous():
            # Get the first item's timestamp for previous page
            first_item = data[0] if data else None
            if first_item and hasattr(first_item, 'created_at'):
                prev_timestamp = first_item.created_at.isoformat()
                previous_url = f"{request.build_absolute_uri()}?timestamp={prev_timestamp}&type=new"
        
        return Response({
            'count': self.page.paginator.count,
            'next': next_url,
            'previous': previous_url,
            'results': data
        })
