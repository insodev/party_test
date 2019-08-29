from django.urls import path
from . import views

app_name = 'party-api'

urlpatterns = [
    path('', views.PartyList.as_view(), name='party-list'),
    path('<int:pk>/', views.PartyDetail.as_view(), name='party-detail'),
    path('<int:pk>/register/', views.PartyRegister.as_view(), name='party-register'),
]
