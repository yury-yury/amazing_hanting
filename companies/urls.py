from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from companies import views


urlpatterns = [
    path('<int:pk>/image/', views.CompanyImageView.as_view()),
    ]
