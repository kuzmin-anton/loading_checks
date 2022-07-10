from rest_framework import generics, views
from rest_framework.pagination import PageNumberPagination

from .models import Check
from .serializers import CheckSerializer, CustomerReportSerializer, PurchoseSerializer


class AddCheckAPIView(generics.CreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer


class GetCostsAPIView(views.APIView, PageNumberPagination):
    page_size = 5
    max_page_size = 1000
    page_size_query_param = 'page_size'

    def get_query_set(self):
        customer = self.request.query_params['customer_id']
        start_date = self.request.query_params['start_date']
        end_date = self.request.query_params['end_date']
        costs = Check.objects.filter(check_issuance_time__range=[
            start_date, end_date], customer_id__exact=customer)
        return self.paginate_queryset(costs, self.request)

    def get(self, request):
        serializer = PurchoseSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        costs = self.get_query_set()
        result = CustomerReportSerializer(costs, many=True).data
        return self.get_paginated_response(result)
