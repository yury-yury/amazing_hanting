"""amazing_hinting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from vacancies import views
from vacancies.views import SkillsViewSet

router = routers.SimpleRouter()
router.register('skill', SkillsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('hello/', views.hello),
    # path('vacancy/', views.index),
    # path('vacancy/', views.VacancyView.as_view()),
    # path('vacancy/<int:vacancy_id>/', views.get),
    # path('vacancy/', views.VacancyListView.as_view()),
    # path('vacancy/<int:pk>/', views.VacancyDetailView.as_view()),
    # path('vacancy/create/', views.VacancyCreateView.as_view()),
    # path('vacancy/<int:pk>/update/', views.VacancyUpdateView.as_view()),
    # path('vacancy/<int:pk>/delete/', views.VacancyDeleteView.as_view()),
    path('vacancy/', include('vacancies.urls')),
    path('company/', include('companies.urls')),
    path('user/', include('authentication.urls')),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)