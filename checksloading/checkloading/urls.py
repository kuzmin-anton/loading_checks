from django.urls import path

from . import views


urlpatterns = [
    path('add_check/', views.AddCheckAPIView.as_view(), name='add_check'),
    path('get_costs/', views.GetCostsAPIView.as_view(),
         name='get_costs')
]
