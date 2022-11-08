"""LITReview URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from Webapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('registered/', views.registered, name='registered'),
    path('ticket/', views.ticket_create, name='ticket-create'),
    path('ticket/<int:ticket_id>/', views.ticket, name='ticket-profil'),
    path('ticket/<int:ticket_id>/change/', views.ticket_change, name='ticket-change'),
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket-delete'),
    path('review/create/<int:ticket_id>/', views.review_create, name='review-create'),
    path('review/<int:review_id>/', views.review, name='review-profil'),
    path('review/<int:review_id>/change/', views.review_change, name='review-change'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review-delete'),
    path('posts/', views.posts, name='posts'),
    path('follows/', views.follows, name='follows'),
    path('follows/<int:follow_id>/', views.follow_delete, name='follow-delete')
]
urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)