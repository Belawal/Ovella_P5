from django.urls import path, include
from. import views

urlpatterns = [
    path('',views.index, name='home'),
    path('info/', views.info_page, name='info_page'),
]
