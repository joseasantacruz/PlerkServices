from django.urls import path
from api.views import *
from django.contrib import admin

app_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('company', Company_APIView.as_view()),
    path('company/<int:pk>/', Company_APIView_Detail.as_view()),
    path('transaction', Transaction_APIView.as_view()),
    path('transaction/<int:pk>/', Transaction_APIView_Detail.as_view()),
    path('summary', Summary_APIView.as_view()),
    path('company/<int:pk>/summary', Company_Summary_APIView.as_view()),
]